# NadLan3D Lovable Implementation Plan - 1000 Steps

Status: owner-facing execution plan, not a claim that the site is fixed.

Honesty statement: this file is a control plan. It does not replace live screenshots, release verification, or WordPress deployment proof. If I claim something is done later, the matching proof must exist in GitHub, the live site, or docs/qa/screenshots.

How to use this plan: follow steps in order inside each slice. Each row states the action, source proof set, code or proof example, expected false-claim risk, how the owner can catch it, and how I must fix it.

## Source Index

- S01: WordPress wp_add_inline_style order. https://developer.wordpress.org/reference/functions/wp_add_inline_style/. Inline CSS blocks attached to a handle print in insertion order, so later inline CSS can silently repaint earlier CSS.
- S02: WordPress wp_enqueue_style versioning. https://developer.wordpress.org/reference/functions/wp_enqueue_style/. External stylesheets should be enqueued with explicit handles and versions so cache-busting is measurable.
- S03: MDN CSS cascade. https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Introduction. Specificity, origin, importance and source order decide which CSS wins.
- S04: CSS Wizardry Three I refactor method. https://csswizardry.com/2016/08/refactoring-css-the-three-i-s/. CSS refactoring should identify, isolate and implement, not blindly override.
- S05: Smashing CSS refactoring and regression testing. https://www.smashingmagazine.com/2021/08/refactoring-css-strategy-regression-testing-maintenance-part2/. CSS refactors need target goals, incremental strategy and visual regression proof.
- S06: Playwright screenshots. https://playwright.dev/docs/screenshots. Screenshots are the visual proof artifact for browser state.
- S07: Playwright visual comparisons. https://playwright.dev/docs/test-snapshots. Visual changes should be compared against stable screenshots when possible.
- S08: model-viewer docs. https://modelviewer.dev/docs/. camera-orbit and camera-target are supported model-viewer controls.
- S09: model-viewer annotations. https://modelviewer.dev/examples/annotations. Hotspots are child elements with slots beginning with hotspot.
- S10: WordPress Plugin Handbook. https://developer.wordpress.org/plugins/. Plugin work needs predictable architecture, hooks, lifecycle and release discipline.
- S11: WordPress sanitizing. https://developer.wordpress.org/apis/security/sanitizing/. Untrusted input needs validation and sanitization before storage or use.
- S12: WordPress Plugin Check. https://wordpress.org/plugins/plugin-check/. Plugin Check can be run via WP Admin or WP-CLI and covers quality categories.
- S13: W3C WCAG 2.2. https://www.w3.org/TR/WCAG22/. Accessibility requirements cover contrast, keyboard, touch targets and understandable UI.
- S14: Google structured data. https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data. Structured data helps Google understand page content when it matches real page content.
- S15: Git hooks. https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks. Hooks can block unsafe pushes by exiting non-zero.
- S16: NadLan master skill. skills/nadlan-autonomous-execution-master.md. Local rule: no stacking, no fake proof, screenshots before claims, guarded plugin releases.
- S17: Lovable premium packet. handoff/lovable/2026-06-24-premium-pattern/README.md. Local packet: static reference, not live WordPress. PR 1 is showroom premium visual replacement.
- S18: Lovable implementation map. handoff/lovable/2026-06-24-premium-pattern/08-wordpress-implementation-map.md. Local map: stop old active style, emit premium classes, load premium stylesheet, keep behavior stable.

## Phase Map

- 001-020: Ground Truth and Trust Reset. Goal: Inspect actual GitHub, local files, ZIP, current live page, current plugin version and current broken points before touching code.. Source set: S16,S17.
- 021-060: Lovable Packet Inventory. Goal: Map every Lovable doc, screenshot, reference file and JSON contract to a WordPress implementation target.. Source set: S17,S18.
- 061-100: Repo and Plugin Triage. Goal: Identify active theme, custom plugin, enqueue paths, render functions, version surfaces and release artifacts.. Source set: S10,S16.
- 101-160: No-Stacking CSS Replacement. Goal: Remove or stop old active visual sources before loading the premium skin.. Source set: S01,S02,S03,S04,S05,S18.
- 161-220: Showroom Markup Replacement. Goal: Translate reference/showroom-reference.html into existing PHP output without breaking data, REST or selection behavior.. Source set: S10,S11,S17,S18.
- 221-300: Premium Showroom CSS. Goal: Move Lovable cream tokens into one primary showroom stylesheet and prevent old dark repaint.. Source set: S01,S02,S03,S04,S05,S13,S17.
- 301-360: 3D Model and Apartment Selection. Goal: Keep authored-unit and row-aligned tap behavior, verify camera-orbit and camera-target, avoid false exact-BIM claims.. Source set: S08,S09,S16,S17.
- 361-420: Mobile 390 and RTL Layout. Goal: Prove no horizontal overflow, correct Hebrew RTL, usable controls and no hidden broken right edge.. Source set: S06,S07,S13,S16.
- 421-480: Public Language Cleanup. Goal: Remove internal labels and buyer-facing technical words, keep contractor technical terms only in admin/contractor context.. Source set: S13,S16,S17.
- 481-540: Release 1.69.x Packaging. Goal: Bump all version surfaces, build guarded ZIP, verify ZIP paths, versions, cache busters and manifest.. Source set: S02,S10,S12,S15,S16.
- 541-600: Live Deploy and Recovery. Goal: Deploy only verified artifacts, flush permalinks if routes break, verify healthcheck and live screenshots.. Source set: S10,S12,S16.
- 601-660: Projects Archive Premium Shelf. Goal: Apply Lovable projects reference to /projects/ after showroom is stable, with real cards and no ranking-label leaks.. Source set: S03,S05,S13,S17.
- 661-720: Homepage Premium Brand Shell. Goal: Apply homepage reference after showroom and projects, with NadLan3D first viewport and clear buyer/developer paths.. Source set: S03,S05,S13,S17.
- 721-780: Brand Assets and Favicon. Goal: Install favicon, app icons, OG card and wordmark with proof from browser tab and page source.. Source set: S02,S06,S13,S17.
- 781-840: SEO and Structured Data. Goal: Protect canonical page intent, schema truth, internal linking and project/city/listing separation.. Source set: S14,S16,S17.
- 841-900: Admin War Room. Goal: Make strategy packets visible inside WordPress admin, private and readable, without public leakage.. Source set: S10,S11,S16.
- 901-940: Skills and Process Capture. Goal: Update master skill and shared skills with what succeeded, what failed, and what must be checked next time.. Source set: S15,S16.
- 941-980: Full QA Gallery. Goal: Capture desktop, mobile, Hebrew, English, selection, missing asset, route, health and public-language proof.. Source set: S06,S07,S13,S16.
- 981-1000: Owner Demo Readiness. Goal: Produce a final showable path, honest limitations, rollback notes and exact next investment inputs needed.. Source set: S16,S17,S18.

## The 1000 Steps

### 001. Ground Truth and Trust Reset
- Action: List local modified and untracked files before touching more code.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 002. Ground Truth and Trust Reset
- Action: Confirm GitHub main contains the imported Lovable packet.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 003. Ground Truth and Trust Reset
- Action: Open the live Rainbow page and record what actually renders.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 004. Ground Truth and Trust Reset
- Action: Read the Lovable README and implementation map again.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 005. Ground Truth and Trust Reset
- Action: Write the current known truth in one sentence before editing.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 006. Ground Truth and Trust Reset
- Action: List local modified and untracked files before touching more code.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 007. Ground Truth and Trust Reset
- Action: Confirm GitHub main contains the imported Lovable packet.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 008. Ground Truth and Trust Reset
- Action: Open the live Rainbow page and record what actually renders.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 009. Ground Truth and Trust Reset
- Action: Read the Lovable README and implementation map again.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 010. Ground Truth and Trust Reset
- Action: Write the current known truth in one sentence before editing.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 011. Ground Truth and Trust Reset
- Action: List local modified and untracked files before touching more code.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 012. Ground Truth and Trust Reset
- Action: Confirm GitHub main contains the imported Lovable packet.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 013. Ground Truth and Trust Reset
- Action: Open the live Rainbow page and record what actually renders.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 014. Ground Truth and Trust Reset
- Action: Read the Lovable README and implementation map again.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 015. Ground Truth and Trust Reset
- Action: Write the current known truth in one sentence before editing.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 016. Ground Truth and Trust Reset
- Action: List local modified and untracked files before touching more code.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 017. Ground Truth and Trust Reset
- Action: Confirm GitHub main contains the imported Lovable packet.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 018. Ground Truth and Trust Reset
- Action: Open the live Rainbow page and record what actually renders.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 019. Ground Truth and Trust Reset
- Action: Read the Lovable README and implementation map again.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 020. Ground Truth and Trust Reset
- Action: Write the current known truth in one sentence before editing.
- Research proof set: S16,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 021. Lovable Packet Inventory
- Action: Map one Lovable reference file to one WordPress target.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 022. Lovable Packet Inventory
- Action: Compare one Lovable screenshot to the current live page.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 023. Lovable Packet Inventory
- Action: Record whether a screenshot is static reference or live WordPress proof.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 024. Lovable Packet Inventory
- Action: Extract a token, component or QA rule from the packet.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 025. Lovable Packet Inventory
- Action: Mark one missing contractor input honestly.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 026. Lovable Packet Inventory
- Action: Map one Lovable reference file to one WordPress target.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 027. Lovable Packet Inventory
- Action: Compare one Lovable screenshot to the current live page.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 028. Lovable Packet Inventory
- Action: Record whether a screenshot is static reference or live WordPress proof.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 029. Lovable Packet Inventory
- Action: Extract a token, component or QA rule from the packet.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 030. Lovable Packet Inventory
- Action: Mark one missing contractor input honestly.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 031. Lovable Packet Inventory
- Action: Map one Lovable reference file to one WordPress target.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 032. Lovable Packet Inventory
- Action: Compare one Lovable screenshot to the current live page.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 033. Lovable Packet Inventory
- Action: Record whether a screenshot is static reference or live WordPress proof.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 034. Lovable Packet Inventory
- Action: Extract a token, component or QA rule from the packet.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 035. Lovable Packet Inventory
- Action: Mark one missing contractor input honestly.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 036. Lovable Packet Inventory
- Action: Map one Lovable reference file to one WordPress target.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 037. Lovable Packet Inventory
- Action: Compare one Lovable screenshot to the current live page.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 038. Lovable Packet Inventory
- Action: Record whether a screenshot is static reference or live WordPress proof.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 039. Lovable Packet Inventory
- Action: Extract a token, component or QA rule from the packet.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 040. Lovable Packet Inventory
- Action: Mark one missing contractor input honestly.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 041. Lovable Packet Inventory
- Action: Map one Lovable reference file to one WordPress target.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 042. Lovable Packet Inventory
- Action: Compare one Lovable screenshot to the current live page.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 043. Lovable Packet Inventory
- Action: Record whether a screenshot is static reference or live WordPress proof.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 044. Lovable Packet Inventory
- Action: Extract a token, component or QA rule from the packet.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 045. Lovable Packet Inventory
- Action: Mark one missing contractor input honestly.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 046. Lovable Packet Inventory
- Action: Map one Lovable reference file to one WordPress target.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 047. Lovable Packet Inventory
- Action: Compare one Lovable screenshot to the current live page.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 048. Lovable Packet Inventory
- Action: Record whether a screenshot is static reference or live WordPress proof.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 049. Lovable Packet Inventory
- Action: Extract a token, component or QA rule from the packet.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 050. Lovable Packet Inventory
- Action: Mark one missing contractor input honestly.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 051. Lovable Packet Inventory
- Action: Map one Lovable reference file to one WordPress target.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 052. Lovable Packet Inventory
- Action: Compare one Lovable screenshot to the current live page.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 053. Lovable Packet Inventory
- Action: Record whether a screenshot is static reference or live WordPress proof.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 054. Lovable Packet Inventory
- Action: Extract a token, component or QA rule from the packet.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 055. Lovable Packet Inventory
- Action: Mark one missing contractor input honestly.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 056. Lovable Packet Inventory
- Action: Map one Lovable reference file to one WordPress target.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 057. Lovable Packet Inventory
- Action: Compare one Lovable screenshot to the current live page.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 058. Lovable Packet Inventory
- Action: Record whether a screenshot is static reference or live WordPress proof.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 059. Lovable Packet Inventory
- Action: Extract a token, component or QA rule from the packet.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 060. Lovable Packet Inventory
- Action: Mark one missing contractor input honestly.
- Research proof set: S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 061. Repo and Plugin Triage
- Action: Search for active enqueue and render functions.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 062. Repo and Plugin Triage
- Action: Find all version surfaces before release work.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 063. Repo and Plugin Triage
- Action: Identify which files own public markup.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 064. Repo and Plugin Triage
- Action: Confirm the plugin path manually because automatic triage missed it.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 065. Repo and Plugin Triage
- Action: Inspect current ZIP and manifest ownership.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 066. Repo and Plugin Triage
- Action: Search for active enqueue and render functions.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 067. Repo and Plugin Triage
- Action: Find all version surfaces before release work.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 068. Repo and Plugin Triage
- Action: Identify which files own public markup.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 069. Repo and Plugin Triage
- Action: Confirm the plugin path manually because automatic triage missed it.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 070. Repo and Plugin Triage
- Action: Inspect current ZIP and manifest ownership.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 071. Repo and Plugin Triage
- Action: Search for active enqueue and render functions.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 072. Repo and Plugin Triage
- Action: Find all version surfaces before release work.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 073. Repo and Plugin Triage
- Action: Identify which files own public markup.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 074. Repo and Plugin Triage
- Action: Confirm the plugin path manually because automatic triage missed it.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 075. Repo and Plugin Triage
- Action: Inspect current ZIP and manifest ownership.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 076. Repo and Plugin Triage
- Action: Search for active enqueue and render functions.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 077. Repo and Plugin Triage
- Action: Find all version surfaces before release work.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 078. Repo and Plugin Triage
- Action: Identify which files own public markup.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 079. Repo and Plugin Triage
- Action: Confirm the plugin path manually because automatic triage missed it.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 080. Repo and Plugin Triage
- Action: Inspect current ZIP and manifest ownership.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 081. Repo and Plugin Triage
- Action: Search for active enqueue and render functions.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 082. Repo and Plugin Triage
- Action: Find all version surfaces before release work.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 083. Repo and Plugin Triage
- Action: Identify which files own public markup.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 084. Repo and Plugin Triage
- Action: Confirm the plugin path manually because automatic triage missed it.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 085. Repo and Plugin Triage
- Action: Inspect current ZIP and manifest ownership.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 086. Repo and Plugin Triage
- Action: Search for active enqueue and render functions.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 087. Repo and Plugin Triage
- Action: Find all version surfaces before release work.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 088. Repo and Plugin Triage
- Action: Identify which files own public markup.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 089. Repo and Plugin Triage
- Action: Confirm the plugin path manually because automatic triage missed it.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 090. Repo and Plugin Triage
- Action: Inspect current ZIP and manifest ownership.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 091. Repo and Plugin Triage
- Action: Search for active enqueue and render functions.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 092. Repo and Plugin Triage
- Action: Find all version surfaces before release work.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 093. Repo and Plugin Triage
- Action: Identify which files own public markup.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 094. Repo and Plugin Triage
- Action: Confirm the plugin path manually because automatic triage missed it.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 095. Repo and Plugin Triage
- Action: Inspect current ZIP and manifest ownership.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 096. Repo and Plugin Triage
- Action: Search for active enqueue and render functions.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 097. Repo and Plugin Triage
- Action: Find all version surfaces before release work.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 098. Repo and Plugin Triage
- Action: Identify which files own public markup.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 099. Repo and Plugin Triage
- Action: Confirm the plugin path manually because automatic triage missed it.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 100. Repo and Plugin Triage
- Action: Inspect current ZIP and manifest ownership.
- Research proof set: S10,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 101. No-Stacking CSS Replacement
- Action: Identify one old active CSS source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 102. No-Stacking CSS Replacement
- Action: Stop loading one old visual source before adding the replacement.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 103. No-Stacking CSS Replacement
- Action: Move one visual rule into the primary premium stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 104. No-Stacking CSS Replacement
- Action: Search for dark hardcoded colors that still repaint the showroom.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 105. No-Stacking CSS Replacement
- Action: Prove no late inline block overrides the premium source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 106. No-Stacking CSS Replacement
- Action: Identify one old active CSS source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 107. No-Stacking CSS Replacement
- Action: Stop loading one old visual source before adding the replacement.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 108. No-Stacking CSS Replacement
- Action: Move one visual rule into the primary premium stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 109. No-Stacking CSS Replacement
- Action: Search for dark hardcoded colors that still repaint the showroom.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 110. No-Stacking CSS Replacement
- Action: Prove no late inline block overrides the premium source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 111. No-Stacking CSS Replacement
- Action: Identify one old active CSS source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 112. No-Stacking CSS Replacement
- Action: Stop loading one old visual source before adding the replacement.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 113. No-Stacking CSS Replacement
- Action: Move one visual rule into the primary premium stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 114. No-Stacking CSS Replacement
- Action: Search for dark hardcoded colors that still repaint the showroom.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 115. No-Stacking CSS Replacement
- Action: Prove no late inline block overrides the premium source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 116. No-Stacking CSS Replacement
- Action: Identify one old active CSS source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 117. No-Stacking CSS Replacement
- Action: Stop loading one old visual source before adding the replacement.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 118. No-Stacking CSS Replacement
- Action: Move one visual rule into the primary premium stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 119. No-Stacking CSS Replacement
- Action: Search for dark hardcoded colors that still repaint the showroom.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 120. No-Stacking CSS Replacement
- Action: Prove no late inline block overrides the premium source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 121. No-Stacking CSS Replacement
- Action: Identify one old active CSS source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 122. No-Stacking CSS Replacement
- Action: Stop loading one old visual source before adding the replacement.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 123. No-Stacking CSS Replacement
- Action: Move one visual rule into the primary premium stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 124. No-Stacking CSS Replacement
- Action: Search for dark hardcoded colors that still repaint the showroom.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 125. No-Stacking CSS Replacement
- Action: Prove no late inline block overrides the premium source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 126. No-Stacking CSS Replacement
- Action: Identify one old active CSS source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 127. No-Stacking CSS Replacement
- Action: Stop loading one old visual source before adding the replacement.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 128. No-Stacking CSS Replacement
- Action: Move one visual rule into the primary premium stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 129. No-Stacking CSS Replacement
- Action: Search for dark hardcoded colors that still repaint the showroom.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 130. No-Stacking CSS Replacement
- Action: Prove no late inline block overrides the premium source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 131. No-Stacking CSS Replacement
- Action: Identify one old active CSS source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 132. No-Stacking CSS Replacement
- Action: Stop loading one old visual source before adding the replacement.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 133. No-Stacking CSS Replacement
- Action: Move one visual rule into the primary premium stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 134. No-Stacking CSS Replacement
- Action: Search for dark hardcoded colors that still repaint the showroom.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 135. No-Stacking CSS Replacement
- Action: Prove no late inline block overrides the premium source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 136. No-Stacking CSS Replacement
- Action: Identify one old active CSS source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 137. No-Stacking CSS Replacement
- Action: Stop loading one old visual source before adding the replacement.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 138. No-Stacking CSS Replacement
- Action: Move one visual rule into the primary premium stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 139. No-Stacking CSS Replacement
- Action: Search for dark hardcoded colors that still repaint the showroom.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 140. No-Stacking CSS Replacement
- Action: Prove no late inline block overrides the premium source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 141. No-Stacking CSS Replacement
- Action: Identify one old active CSS source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 142. No-Stacking CSS Replacement
- Action: Stop loading one old visual source before adding the replacement.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 143. No-Stacking CSS Replacement
- Action: Move one visual rule into the primary premium stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 144. No-Stacking CSS Replacement
- Action: Search for dark hardcoded colors that still repaint the showroom.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 145. No-Stacking CSS Replacement
- Action: Prove no late inline block overrides the premium source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 146. No-Stacking CSS Replacement
- Action: Identify one old active CSS source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 147. No-Stacking CSS Replacement
- Action: Stop loading one old visual source before adding the replacement.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 148. No-Stacking CSS Replacement
- Action: Move one visual rule into the primary premium stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 149. No-Stacking CSS Replacement
- Action: Search for dark hardcoded colors that still repaint the showroom.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 150. No-Stacking CSS Replacement
- Action: Prove no late inline block overrides the premium source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 151. No-Stacking CSS Replacement
- Action: Identify one old active CSS source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 152. No-Stacking CSS Replacement
- Action: Stop loading one old visual source before adding the replacement.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 153. No-Stacking CSS Replacement
- Action: Move one visual rule into the primary premium stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 154. No-Stacking CSS Replacement
- Action: Search for dark hardcoded colors that still repaint the showroom.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 155. No-Stacking CSS Replacement
- Action: Prove no late inline block overrides the premium source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 156. No-Stacking CSS Replacement
- Action: Identify one old active CSS source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 157. No-Stacking CSS Replacement
- Action: Stop loading one old visual source before adding the replacement.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 158. No-Stacking CSS Replacement
- Action: Move one visual rule into the primary premium stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 159. No-Stacking CSS Replacement
- Action: Search for dark hardcoded colors that still repaint the showroom.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 160. No-Stacking CSS Replacement
- Action: Prove no late inline block overrides the premium source.
- Research proof set: S01,S02,S03,S04,S05,S18.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 161. Showroom Markup Replacement
- Action: Replace one old duplicate section with the premium structure.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 162. Showroom Markup Replacement
- Action: Keep data attributes required by current JavaScript.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 163. Showroom Markup Replacement
- Action: Add one Lovable class without breaking existing selectors.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 164. Showroom Markup Replacement
- Action: Remove one duplicate CTA or intro block from public DOM.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 165. Showroom Markup Replacement
- Action: Escape one piece of dynamic output correctly.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 166. Showroom Markup Replacement
- Action: Replace one old duplicate section with the premium structure.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 167. Showroom Markup Replacement
- Action: Keep data attributes required by current JavaScript.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 168. Showroom Markup Replacement
- Action: Add one Lovable class without breaking existing selectors.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 169. Showroom Markup Replacement
- Action: Remove one duplicate CTA or intro block from public DOM.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 170. Showroom Markup Replacement
- Action: Escape one piece of dynamic output correctly.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 171. Showroom Markup Replacement
- Action: Replace one old duplicate section with the premium structure.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 172. Showroom Markup Replacement
- Action: Keep data attributes required by current JavaScript.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 173. Showroom Markup Replacement
- Action: Add one Lovable class without breaking existing selectors.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 174. Showroom Markup Replacement
- Action: Remove one duplicate CTA or intro block from public DOM.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 175. Showroom Markup Replacement
- Action: Escape one piece of dynamic output correctly.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 176. Showroom Markup Replacement
- Action: Replace one old duplicate section with the premium structure.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 177. Showroom Markup Replacement
- Action: Keep data attributes required by current JavaScript.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 178. Showroom Markup Replacement
- Action: Add one Lovable class without breaking existing selectors.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 179. Showroom Markup Replacement
- Action: Remove one duplicate CTA or intro block from public DOM.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 180. Showroom Markup Replacement
- Action: Escape one piece of dynamic output correctly.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 181. Showroom Markup Replacement
- Action: Replace one old duplicate section with the premium structure.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 182. Showroom Markup Replacement
- Action: Keep data attributes required by current JavaScript.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 183. Showroom Markup Replacement
- Action: Add one Lovable class without breaking existing selectors.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 184. Showroom Markup Replacement
- Action: Remove one duplicate CTA or intro block from public DOM.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 185. Showroom Markup Replacement
- Action: Escape one piece of dynamic output correctly.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 186. Showroom Markup Replacement
- Action: Replace one old duplicate section with the premium structure.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 187. Showroom Markup Replacement
- Action: Keep data attributes required by current JavaScript.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 188. Showroom Markup Replacement
- Action: Add one Lovable class without breaking existing selectors.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 189. Showroom Markup Replacement
- Action: Remove one duplicate CTA or intro block from public DOM.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 190. Showroom Markup Replacement
- Action: Escape one piece of dynamic output correctly.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 191. Showroom Markup Replacement
- Action: Replace one old duplicate section with the premium structure.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 192. Showroom Markup Replacement
- Action: Keep data attributes required by current JavaScript.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 193. Showroom Markup Replacement
- Action: Add one Lovable class without breaking existing selectors.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 194. Showroom Markup Replacement
- Action: Remove one duplicate CTA or intro block from public DOM.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 195. Showroom Markup Replacement
- Action: Escape one piece of dynamic output correctly.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 196. Showroom Markup Replacement
- Action: Replace one old duplicate section with the premium structure.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 197. Showroom Markup Replacement
- Action: Keep data attributes required by current JavaScript.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 198. Showroom Markup Replacement
- Action: Add one Lovable class without breaking existing selectors.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 199. Showroom Markup Replacement
- Action: Remove one duplicate CTA or intro block from public DOM.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 200. Showroom Markup Replacement
- Action: Escape one piece of dynamic output correctly.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 201. Showroom Markup Replacement
- Action: Replace one old duplicate section with the premium structure.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 202. Showroom Markup Replacement
- Action: Keep data attributes required by current JavaScript.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 203. Showroom Markup Replacement
- Action: Add one Lovable class without breaking existing selectors.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 204. Showroom Markup Replacement
- Action: Remove one duplicate CTA or intro block from public DOM.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 205. Showroom Markup Replacement
- Action: Escape one piece of dynamic output correctly.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 206. Showroom Markup Replacement
- Action: Replace one old duplicate section with the premium structure.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 207. Showroom Markup Replacement
- Action: Keep data attributes required by current JavaScript.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 208. Showroom Markup Replacement
- Action: Add one Lovable class without breaking existing selectors.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 209. Showroom Markup Replacement
- Action: Remove one duplicate CTA or intro block from public DOM.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 210. Showroom Markup Replacement
- Action: Escape one piece of dynamic output correctly.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 211. Showroom Markup Replacement
- Action: Replace one old duplicate section with the premium structure.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 212. Showroom Markup Replacement
- Action: Keep data attributes required by current JavaScript.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 213. Showroom Markup Replacement
- Action: Add one Lovable class without breaking existing selectors.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 214. Showroom Markup Replacement
- Action: Remove one duplicate CTA or intro block from public DOM.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 215. Showroom Markup Replacement
- Action: Escape one piece of dynamic output correctly.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 216. Showroom Markup Replacement
- Action: Replace one old duplicate section with the premium structure.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 217. Showroom Markup Replacement
- Action: Keep data attributes required by current JavaScript.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 218. Showroom Markup Replacement
- Action: Add one Lovable class without breaking existing selectors.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 219. Showroom Markup Replacement
- Action: Remove one duplicate CTA or intro block from public DOM.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 220. Showroom Markup Replacement
- Action: Escape one piece of dynamic output correctly.
- Research proof set: S10,S11,S17,S18.
- Code or proof example: `<section class="nlp3d nlp3d-premium nl3d-page">...</section>`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 221. Premium Showroom CSS
- Action: Apply one Lovable token to the new stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 222. Premium Showroom CSS
- Action: Style one active showroom component from the reference packet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 223. Premium Showroom CSS
- Action: Remove one unnecessary important override.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 224. Premium Showroom CSS
- Action: Check one mobile breakpoint against 390 width.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 225. Premium Showroom CSS
- Action: Verify cream skin owns the stage background.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 226. Premium Showroom CSS
- Action: Apply one Lovable token to the new stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 227. Premium Showroom CSS
- Action: Style one active showroom component from the reference packet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 228. Premium Showroom CSS
- Action: Remove one unnecessary important override.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 229. Premium Showroom CSS
- Action: Check one mobile breakpoint against 390 width.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 230. Premium Showroom CSS
- Action: Verify cream skin owns the stage background.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 231. Premium Showroom CSS
- Action: Apply one Lovable token to the new stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 232. Premium Showroom CSS
- Action: Style one active showroom component from the reference packet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 233. Premium Showroom CSS
- Action: Remove one unnecessary important override.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 234. Premium Showroom CSS
- Action: Check one mobile breakpoint against 390 width.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 235. Premium Showroom CSS
- Action: Verify cream skin owns the stage background.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 236. Premium Showroom CSS
- Action: Apply one Lovable token to the new stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 237. Premium Showroom CSS
- Action: Style one active showroom component from the reference packet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 238. Premium Showroom CSS
- Action: Remove one unnecessary important override.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 239. Premium Showroom CSS
- Action: Check one mobile breakpoint against 390 width.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 240. Premium Showroom CSS
- Action: Verify cream skin owns the stage background.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 241. Premium Showroom CSS
- Action: Apply one Lovable token to the new stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 242. Premium Showroom CSS
- Action: Style one active showroom component from the reference packet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 243. Premium Showroom CSS
- Action: Remove one unnecessary important override.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 244. Premium Showroom CSS
- Action: Check one mobile breakpoint against 390 width.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 245. Premium Showroom CSS
- Action: Verify cream skin owns the stage background.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 246. Premium Showroom CSS
- Action: Apply one Lovable token to the new stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 247. Premium Showroom CSS
- Action: Style one active showroom component from the reference packet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 248. Premium Showroom CSS
- Action: Remove one unnecessary important override.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 249. Premium Showroom CSS
- Action: Check one mobile breakpoint against 390 width.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 250. Premium Showroom CSS
- Action: Verify cream skin owns the stage background.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 251. Premium Showroom CSS
- Action: Apply one Lovable token to the new stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 252. Premium Showroom CSS
- Action: Style one active showroom component from the reference packet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 253. Premium Showroom CSS
- Action: Remove one unnecessary important override.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 254. Premium Showroom CSS
- Action: Check one mobile breakpoint against 390 width.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 255. Premium Showroom CSS
- Action: Verify cream skin owns the stage background.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 256. Premium Showroom CSS
- Action: Apply one Lovable token to the new stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 257. Premium Showroom CSS
- Action: Style one active showroom component from the reference packet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 258. Premium Showroom CSS
- Action: Remove one unnecessary important override.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 259. Premium Showroom CSS
- Action: Check one mobile breakpoint against 390 width.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 260. Premium Showroom CSS
- Action: Verify cream skin owns the stage background.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 261. Premium Showroom CSS
- Action: Apply one Lovable token to the new stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 262. Premium Showroom CSS
- Action: Style one active showroom component from the reference packet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 263. Premium Showroom CSS
- Action: Remove one unnecessary important override.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 264. Premium Showroom CSS
- Action: Check one mobile breakpoint against 390 width.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 265. Premium Showroom CSS
- Action: Verify cream skin owns the stage background.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 266. Premium Showroom CSS
- Action: Apply one Lovable token to the new stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 267. Premium Showroom CSS
- Action: Style one active showroom component from the reference packet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 268. Premium Showroom CSS
- Action: Remove one unnecessary important override.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 269. Premium Showroom CSS
- Action: Check one mobile breakpoint against 390 width.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 270. Premium Showroom CSS
- Action: Verify cream skin owns the stage background.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 271. Premium Showroom CSS
- Action: Apply one Lovable token to the new stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 272. Premium Showroom CSS
- Action: Style one active showroom component from the reference packet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 273. Premium Showroom CSS
- Action: Remove one unnecessary important override.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 274. Premium Showroom CSS
- Action: Check one mobile breakpoint against 390 width.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 275. Premium Showroom CSS
- Action: Verify cream skin owns the stage background.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 276. Premium Showroom CSS
- Action: Apply one Lovable token to the new stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 277. Premium Showroom CSS
- Action: Style one active showroom component from the reference packet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 278. Premium Showroom CSS
- Action: Remove one unnecessary important override.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 279. Premium Showroom CSS
- Action: Check one mobile breakpoint against 390 width.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 280. Premium Showroom CSS
- Action: Verify cream skin owns the stage background.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 281. Premium Showroom CSS
- Action: Apply one Lovable token to the new stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 282. Premium Showroom CSS
- Action: Style one active showroom component from the reference packet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 283. Premium Showroom CSS
- Action: Remove one unnecessary important override.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 284. Premium Showroom CSS
- Action: Check one mobile breakpoint against 390 width.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 285. Premium Showroom CSS
- Action: Verify cream skin owns the stage background.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 286. Premium Showroom CSS
- Action: Apply one Lovable token to the new stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 287. Premium Showroom CSS
- Action: Style one active showroom component from the reference packet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 288. Premium Showroom CSS
- Action: Remove one unnecessary important override.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 289. Premium Showroom CSS
- Action: Check one mobile breakpoint against 390 width.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 290. Premium Showroom CSS
- Action: Verify cream skin owns the stage background.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 291. Premium Showroom CSS
- Action: Apply one Lovable token to the new stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 292. Premium Showroom CSS
- Action: Style one active showroom component from the reference packet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 293. Premium Showroom CSS
- Action: Remove one unnecessary important override.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 294. Premium Showroom CSS
- Action: Check one mobile breakpoint against 390 width.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 295. Premium Showroom CSS
- Action: Verify cream skin owns the stage background.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 296. Premium Showroom CSS
- Action: Apply one Lovable token to the new stylesheet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 297. Premium Showroom CSS
- Action: Style one active showroom component from the reference packet.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 298. Premium Showroom CSS
- Action: Remove one unnecessary important override.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 299. Premium Showroom CSS
- Action: Check one mobile breakpoint against 390 width.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 300. Premium Showroom CSS
- Action: Verify cream skin owns the stage background.
- Research proof set: S01,S02,S03,S04,S05,S13,S17.
- Code or proof example: `wp_enqueue_style('nadlan-p3d', plugins_url('assets/css/project-3d-premium.css', __FILE__), [], '1.69.x');`
- Expected false-claim risk: I may paint over old CSS instead of removing the active old source.
- How you catch it: Catch by checking loaded CSS handles, inline style blocks and hardcoded dark colors in source.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 301. 3D Model and Apartment Selection
- Action: Click or script one real unit selection.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 302. 3D Model and Apartment Selection
- Action: Verify selected unit updates rail, panel and marker.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 303. 3D Model and Apartment Selection
- Action: Verify camera-orbit changes from unit data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 304. 3D Model and Apartment Selection
- Action: Verify camera-target changes from hotspot data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 305. 3D Model and Apartment Selection
- Action: Label exact picking as unavailable unless true geometry exists.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 306. 3D Model and Apartment Selection
- Action: Click or script one real unit selection.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 307. 3D Model and Apartment Selection
- Action: Verify selected unit updates rail, panel and marker.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 308. 3D Model and Apartment Selection
- Action: Verify camera-orbit changes from unit data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 309. 3D Model and Apartment Selection
- Action: Verify camera-target changes from hotspot data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 310. 3D Model and Apartment Selection
- Action: Label exact picking as unavailable unless true geometry exists.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 311. 3D Model and Apartment Selection
- Action: Click or script one real unit selection.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 312. 3D Model and Apartment Selection
- Action: Verify selected unit updates rail, panel and marker.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 313. 3D Model and Apartment Selection
- Action: Verify camera-orbit changes from unit data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 314. 3D Model and Apartment Selection
- Action: Verify camera-target changes from hotspot data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 315. 3D Model and Apartment Selection
- Action: Label exact picking as unavailable unless true geometry exists.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 316. 3D Model and Apartment Selection
- Action: Click or script one real unit selection.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 317. 3D Model and Apartment Selection
- Action: Verify selected unit updates rail, panel and marker.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 318. 3D Model and Apartment Selection
- Action: Verify camera-orbit changes from unit data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 319. 3D Model and Apartment Selection
- Action: Verify camera-target changes from hotspot data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 320. 3D Model and Apartment Selection
- Action: Label exact picking as unavailable unless true geometry exists.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 321. 3D Model and Apartment Selection
- Action: Click or script one real unit selection.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 322. 3D Model and Apartment Selection
- Action: Verify selected unit updates rail, panel and marker.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 323. 3D Model and Apartment Selection
- Action: Verify camera-orbit changes from unit data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 324. 3D Model and Apartment Selection
- Action: Verify camera-target changes from hotspot data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 325. 3D Model and Apartment Selection
- Action: Label exact picking as unavailable unless true geometry exists.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 326. 3D Model and Apartment Selection
- Action: Click or script one real unit selection.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 327. 3D Model and Apartment Selection
- Action: Verify selected unit updates rail, panel and marker.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 328. 3D Model and Apartment Selection
- Action: Verify camera-orbit changes from unit data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 329. 3D Model and Apartment Selection
- Action: Verify camera-target changes from hotspot data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 330. 3D Model and Apartment Selection
- Action: Label exact picking as unavailable unless true geometry exists.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 331. 3D Model and Apartment Selection
- Action: Click or script one real unit selection.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 332. 3D Model and Apartment Selection
- Action: Verify selected unit updates rail, panel and marker.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 333. 3D Model and Apartment Selection
- Action: Verify camera-orbit changes from unit data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 334. 3D Model and Apartment Selection
- Action: Verify camera-target changes from hotspot data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 335. 3D Model and Apartment Selection
- Action: Label exact picking as unavailable unless true geometry exists.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 336. 3D Model and Apartment Selection
- Action: Click or script one real unit selection.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 337. 3D Model and Apartment Selection
- Action: Verify selected unit updates rail, panel and marker.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 338. 3D Model and Apartment Selection
- Action: Verify camera-orbit changes from unit data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 339. 3D Model and Apartment Selection
- Action: Verify camera-target changes from hotspot data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 340. 3D Model and Apartment Selection
- Action: Label exact picking as unavailable unless true geometry exists.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 341. 3D Model and Apartment Selection
- Action: Click or script one real unit selection.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 342. 3D Model and Apartment Selection
- Action: Verify selected unit updates rail, panel and marker.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 343. 3D Model and Apartment Selection
- Action: Verify camera-orbit changes from unit data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 344. 3D Model and Apartment Selection
- Action: Verify camera-target changes from hotspot data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 345. 3D Model and Apartment Selection
- Action: Label exact picking as unavailable unless true geometry exists.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 346. 3D Model and Apartment Selection
- Action: Click or script one real unit selection.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 347. 3D Model and Apartment Selection
- Action: Verify selected unit updates rail, panel and marker.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 348. 3D Model and Apartment Selection
- Action: Verify camera-orbit changes from unit data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 349. 3D Model and Apartment Selection
- Action: Verify camera-target changes from hotspot data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 350. 3D Model and Apartment Selection
- Action: Label exact picking as unavailable unless true geometry exists.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 351. 3D Model and Apartment Selection
- Action: Click or script one real unit selection.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 352. 3D Model and Apartment Selection
- Action: Verify selected unit updates rail, panel and marker.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 353. 3D Model and Apartment Selection
- Action: Verify camera-orbit changes from unit data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 354. 3D Model and Apartment Selection
- Action: Verify camera-target changes from hotspot data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 355. 3D Model and Apartment Selection
- Action: Label exact picking as unavailable unless true geometry exists.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 356. 3D Model and Apartment Selection
- Action: Click or script one real unit selection.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 357. 3D Model and Apartment Selection
- Action: Verify selected unit updates rail, panel and marker.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 358. 3D Model and Apartment Selection
- Action: Verify camera-orbit changes from unit data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 359. 3D Model and Apartment Selection
- Action: Verify camera-target changes from hotspot data.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 360. 3D Model and Apartment Selection
- Action: Label exact picking as unavailable unless true geometry exists.
- Research proof set: S08,S09,S16,S17.
- Code or proof example: `modelViewer.setAttribute('camera-orbit', unit.camera_orbit); modelViewer.setAttribute('camera-target', unit.hotspot_position);`
- Expected false-claim risk: I may claim exact apartment picking when only authored-unit fallback is proven.
- How you catch it: Catch by clicking a unit and comparing selected id, camera-orbit, camera-target and screenshot.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 361. Mobile 390 and RTL Layout
- Action: Run a 390 viewport screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 362. Mobile 390 and RTL Layout
- Action: Check scrollWidth against viewport width.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 363. Mobile 390 and RTL Layout
- Action: Inspect the right edge for clipped Hebrew text.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 364. Mobile 390 and RTL Layout
- Action: Verify touch targets are usable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 365. Mobile 390 and RTL Layout
- Action: Check that selected panel remains readable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 366. Mobile 390 and RTL Layout
- Action: Run a 390 viewport screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 367. Mobile 390 and RTL Layout
- Action: Check scrollWidth against viewport width.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 368. Mobile 390 and RTL Layout
- Action: Inspect the right edge for clipped Hebrew text.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 369. Mobile 390 and RTL Layout
- Action: Verify touch targets are usable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 370. Mobile 390 and RTL Layout
- Action: Check that selected panel remains readable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 371. Mobile 390 and RTL Layout
- Action: Run a 390 viewport screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 372. Mobile 390 and RTL Layout
- Action: Check scrollWidth against viewport width.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 373. Mobile 390 and RTL Layout
- Action: Inspect the right edge for clipped Hebrew text.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 374. Mobile 390 and RTL Layout
- Action: Verify touch targets are usable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 375. Mobile 390 and RTL Layout
- Action: Check that selected panel remains readable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 376. Mobile 390 and RTL Layout
- Action: Run a 390 viewport screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 377. Mobile 390 and RTL Layout
- Action: Check scrollWidth against viewport width.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 378. Mobile 390 and RTL Layout
- Action: Inspect the right edge for clipped Hebrew text.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 379. Mobile 390 and RTL Layout
- Action: Verify touch targets are usable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 380. Mobile 390 and RTL Layout
- Action: Check that selected panel remains readable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 381. Mobile 390 and RTL Layout
- Action: Run a 390 viewport screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 382. Mobile 390 and RTL Layout
- Action: Check scrollWidth against viewport width.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 383. Mobile 390 and RTL Layout
- Action: Inspect the right edge for clipped Hebrew text.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 384. Mobile 390 and RTL Layout
- Action: Verify touch targets are usable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 385. Mobile 390 and RTL Layout
- Action: Check that selected panel remains readable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 386. Mobile 390 and RTL Layout
- Action: Run a 390 viewport screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 387. Mobile 390 and RTL Layout
- Action: Check scrollWidth against viewport width.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 388. Mobile 390 and RTL Layout
- Action: Inspect the right edge for clipped Hebrew text.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 389. Mobile 390 and RTL Layout
- Action: Verify touch targets are usable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 390. Mobile 390 and RTL Layout
- Action: Check that selected panel remains readable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 391. Mobile 390 and RTL Layout
- Action: Run a 390 viewport screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 392. Mobile 390 and RTL Layout
- Action: Check scrollWidth against viewport width.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 393. Mobile 390 and RTL Layout
- Action: Inspect the right edge for clipped Hebrew text.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 394. Mobile 390 and RTL Layout
- Action: Verify touch targets are usable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 395. Mobile 390 and RTL Layout
- Action: Check that selected panel remains readable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 396. Mobile 390 and RTL Layout
- Action: Run a 390 viewport screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 397. Mobile 390 and RTL Layout
- Action: Check scrollWidth against viewport width.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 398. Mobile 390 and RTL Layout
- Action: Inspect the right edge for clipped Hebrew text.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 399. Mobile 390 and RTL Layout
- Action: Verify touch targets are usable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 400. Mobile 390 and RTL Layout
- Action: Check that selected panel remains readable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 401. Mobile 390 and RTL Layout
- Action: Run a 390 viewport screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 402. Mobile 390 and RTL Layout
- Action: Check scrollWidth against viewport width.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 403. Mobile 390 and RTL Layout
- Action: Inspect the right edge for clipped Hebrew text.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 404. Mobile 390 and RTL Layout
- Action: Verify touch targets are usable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 405. Mobile 390 and RTL Layout
- Action: Check that selected panel remains readable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 406. Mobile 390 and RTL Layout
- Action: Run a 390 viewport screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 407. Mobile 390 and RTL Layout
- Action: Check scrollWidth against viewport width.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 408. Mobile 390 and RTL Layout
- Action: Inspect the right edge for clipped Hebrew text.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 409. Mobile 390 and RTL Layout
- Action: Verify touch targets are usable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 410. Mobile 390 and RTL Layout
- Action: Check that selected panel remains readable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 411. Mobile 390 and RTL Layout
- Action: Run a 390 viewport screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 412. Mobile 390 and RTL Layout
- Action: Check scrollWidth against viewport width.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 413. Mobile 390 and RTL Layout
- Action: Inspect the right edge for clipped Hebrew text.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 414. Mobile 390 and RTL Layout
- Action: Verify touch targets are usable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 415. Mobile 390 and RTL Layout
- Action: Check that selected panel remains readable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 416. Mobile 390 and RTL Layout
- Action: Run a 390 viewport screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 417. Mobile 390 and RTL Layout
- Action: Check scrollWidth against viewport width.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 418. Mobile 390 and RTL Layout
- Action: Inspect the right edge for clipped Hebrew text.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 419. Mobile 390 and RTL Layout
- Action: Verify touch targets are usable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 420. Mobile 390 and RTL Layout
- Action: Check that selected panel remains readable.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may crop screenshots and miss right-edge overflow.
- How you catch it: Catch by 390 viewport screenshot plus scrollWidth proof.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 421. Public Language Cleanup
- Action: Scan rendered text for internal words.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 422. Public Language Cleanup
- Action: Replace one buyer-facing technical phrase with buyer language.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 423. Public Language Cleanup
- Action: Keep GLB only in contractor/admin contexts.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 424. Public Language Cleanup
- Action: Remove em dash from new public copy.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 425. Public Language Cleanup
- Action: Verify disclosure language is public-safe.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 426. Public Language Cleanup
- Action: Scan rendered text for internal words.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 427. Public Language Cleanup
- Action: Replace one buyer-facing technical phrase with buyer language.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 428. Public Language Cleanup
- Action: Keep GLB only in contractor/admin contexts.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 429. Public Language Cleanup
- Action: Remove em dash from new public copy.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 430. Public Language Cleanup
- Action: Verify disclosure language is public-safe.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 431. Public Language Cleanup
- Action: Scan rendered text for internal words.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 432. Public Language Cleanup
- Action: Replace one buyer-facing technical phrase with buyer language.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 433. Public Language Cleanup
- Action: Keep GLB only in contractor/admin contexts.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 434. Public Language Cleanup
- Action: Remove em dash from new public copy.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 435. Public Language Cleanup
- Action: Verify disclosure language is public-safe.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 436. Public Language Cleanup
- Action: Scan rendered text for internal words.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 437. Public Language Cleanup
- Action: Replace one buyer-facing technical phrase with buyer language.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 438. Public Language Cleanup
- Action: Keep GLB only in contractor/admin contexts.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 439. Public Language Cleanup
- Action: Remove em dash from new public copy.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 440. Public Language Cleanup
- Action: Verify disclosure language is public-safe.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 441. Public Language Cleanup
- Action: Scan rendered text for internal words.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 442. Public Language Cleanup
- Action: Replace one buyer-facing technical phrase with buyer language.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 443. Public Language Cleanup
- Action: Keep GLB only in contractor/admin contexts.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 444. Public Language Cleanup
- Action: Remove em dash from new public copy.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 445. Public Language Cleanup
- Action: Verify disclosure language is public-safe.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 446. Public Language Cleanup
- Action: Scan rendered text for internal words.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 447. Public Language Cleanup
- Action: Replace one buyer-facing technical phrase with buyer language.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 448. Public Language Cleanup
- Action: Keep GLB only in contractor/admin contexts.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 449. Public Language Cleanup
- Action: Remove em dash from new public copy.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 450. Public Language Cleanup
- Action: Verify disclosure language is public-safe.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 451. Public Language Cleanup
- Action: Scan rendered text for internal words.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 452. Public Language Cleanup
- Action: Replace one buyer-facing technical phrase with buyer language.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 453. Public Language Cleanup
- Action: Keep GLB only in contractor/admin contexts.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 454. Public Language Cleanup
- Action: Remove em dash from new public copy.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 455. Public Language Cleanup
- Action: Verify disclosure language is public-safe.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 456. Public Language Cleanup
- Action: Scan rendered text for internal words.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 457. Public Language Cleanup
- Action: Replace one buyer-facing technical phrase with buyer language.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 458. Public Language Cleanup
- Action: Keep GLB only in contractor/admin contexts.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 459. Public Language Cleanup
- Action: Remove em dash from new public copy.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 460. Public Language Cleanup
- Action: Verify disclosure language is public-safe.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 461. Public Language Cleanup
- Action: Scan rendered text for internal words.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 462. Public Language Cleanup
- Action: Replace one buyer-facing technical phrase with buyer language.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 463. Public Language Cleanup
- Action: Keep GLB only in contractor/admin contexts.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 464. Public Language Cleanup
- Action: Remove em dash from new public copy.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 465. Public Language Cleanup
- Action: Verify disclosure language is public-safe.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 466. Public Language Cleanup
- Action: Scan rendered text for internal words.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 467. Public Language Cleanup
- Action: Replace one buyer-facing technical phrase with buyer language.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 468. Public Language Cleanup
- Action: Keep GLB only in contractor/admin contexts.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 469. Public Language Cleanup
- Action: Remove em dash from new public copy.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 470. Public Language Cleanup
- Action: Verify disclosure language is public-safe.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 471. Public Language Cleanup
- Action: Scan rendered text for internal words.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 472. Public Language Cleanup
- Action: Replace one buyer-facing technical phrase with buyer language.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 473. Public Language Cleanup
- Action: Keep GLB only in contractor/admin contexts.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 474. Public Language Cleanup
- Action: Remove em dash from new public copy.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 475. Public Language Cleanup
- Action: Verify disclosure language is public-safe.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 476. Public Language Cleanup
- Action: Scan rendered text for internal words.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 477. Public Language Cleanup
- Action: Replace one buyer-facing technical phrase with buyer language.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 478. Public Language Cleanup
- Action: Keep GLB only in contractor/admin contexts.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 479. Public Language Cleanup
- Action: Remove em dash from new public copy.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 480. Public Language Cleanup
- Action: Verify disclosure language is public-safe.
- Research proof set: S13,S16,S17.
- Code or proof example: `rg -n "Lovable|Codex|prompt|token|GLB|SVG|Featured|Sponsored|—" rendered-text.txt`
- Expected false-claim risk: I may leave internal words visible to buyers.
- How you catch it: Catch by rendered text scan and visual review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 481. Release 1.69.x Packaging
- Action: Bump one version surface and cross-check all others.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 482. Release 1.69.x Packaging
- Action: Build the plugin ZIP with the guarded builder.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 483. Release 1.69.x Packaging
- Action: Run the release verifier.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 484. Release 1.69.x Packaging
- Action: Inspect ZIP path separators.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 485. Release 1.69.x Packaging
- Action: Confirm style and script cache-busters match version.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 486. Release 1.69.x Packaging
- Action: Bump one version surface and cross-check all others.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 487. Release 1.69.x Packaging
- Action: Build the plugin ZIP with the guarded builder.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 488. Release 1.69.x Packaging
- Action: Run the release verifier.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 489. Release 1.69.x Packaging
- Action: Inspect ZIP path separators.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 490. Release 1.69.x Packaging
- Action: Confirm style and script cache-busters match version.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 491. Release 1.69.x Packaging
- Action: Bump one version surface and cross-check all others.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 492. Release 1.69.x Packaging
- Action: Build the plugin ZIP with the guarded builder.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 493. Release 1.69.x Packaging
- Action: Run the release verifier.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 494. Release 1.69.x Packaging
- Action: Inspect ZIP path separators.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 495. Release 1.69.x Packaging
- Action: Confirm style and script cache-busters match version.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 496. Release 1.69.x Packaging
- Action: Bump one version surface and cross-check all others.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 497. Release 1.69.x Packaging
- Action: Build the plugin ZIP with the guarded builder.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 498. Release 1.69.x Packaging
- Action: Run the release verifier.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 499. Release 1.69.x Packaging
- Action: Inspect ZIP path separators.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 500. Release 1.69.x Packaging
- Action: Confirm style and script cache-busters match version.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 501. Release 1.69.x Packaging
- Action: Bump one version surface and cross-check all others.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 502. Release 1.69.x Packaging
- Action: Build the plugin ZIP with the guarded builder.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 503. Release 1.69.x Packaging
- Action: Run the release verifier.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 504. Release 1.69.x Packaging
- Action: Inspect ZIP path separators.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 505. Release 1.69.x Packaging
- Action: Confirm style and script cache-busters match version.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 506. Release 1.69.x Packaging
- Action: Bump one version surface and cross-check all others.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 507. Release 1.69.x Packaging
- Action: Build the plugin ZIP with the guarded builder.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 508. Release 1.69.x Packaging
- Action: Run the release verifier.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 509. Release 1.69.x Packaging
- Action: Inspect ZIP path separators.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 510. Release 1.69.x Packaging
- Action: Confirm style and script cache-busters match version.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 511. Release 1.69.x Packaging
- Action: Bump one version surface and cross-check all others.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 512. Release 1.69.x Packaging
- Action: Build the plugin ZIP with the guarded builder.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 513. Release 1.69.x Packaging
- Action: Run the release verifier.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 514. Release 1.69.x Packaging
- Action: Inspect ZIP path separators.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 515. Release 1.69.x Packaging
- Action: Confirm style and script cache-busters match version.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 516. Release 1.69.x Packaging
- Action: Bump one version surface and cross-check all others.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 517. Release 1.69.x Packaging
- Action: Build the plugin ZIP with the guarded builder.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 518. Release 1.69.x Packaging
- Action: Run the release verifier.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 519. Release 1.69.x Packaging
- Action: Inspect ZIP path separators.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 520. Release 1.69.x Packaging
- Action: Confirm style and script cache-busters match version.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 521. Release 1.69.x Packaging
- Action: Bump one version surface and cross-check all others.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 522. Release 1.69.x Packaging
- Action: Build the plugin ZIP with the guarded builder.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 523. Release 1.69.x Packaging
- Action: Run the release verifier.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 524. Release 1.69.x Packaging
- Action: Inspect ZIP path separators.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 525. Release 1.69.x Packaging
- Action: Confirm style and script cache-busters match version.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 526. Release 1.69.x Packaging
- Action: Bump one version surface and cross-check all others.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 527. Release 1.69.x Packaging
- Action: Build the plugin ZIP with the guarded builder.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 528. Release 1.69.x Packaging
- Action: Run the release verifier.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 529. Release 1.69.x Packaging
- Action: Inspect ZIP path separators.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 530. Release 1.69.x Packaging
- Action: Confirm style and script cache-busters match version.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 531. Release 1.69.x Packaging
- Action: Bump one version surface and cross-check all others.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 532. Release 1.69.x Packaging
- Action: Build the plugin ZIP with the guarded builder.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 533. Release 1.69.x Packaging
- Action: Run the release verifier.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 534. Release 1.69.x Packaging
- Action: Inspect ZIP path separators.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 535. Release 1.69.x Packaging
- Action: Confirm style and script cache-busters match version.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 536. Release 1.69.x Packaging
- Action: Bump one version surface and cross-check all others.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 537. Release 1.69.x Packaging
- Action: Build the plugin ZIP with the guarded builder.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 538. Release 1.69.x Packaging
- Action: Run the release verifier.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 539. Release 1.69.x Packaging
- Action: Inspect ZIP path separators.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 540. Release 1.69.x Packaging
- Action: Confirm style and script cache-busters match version.
- Research proof set: S02,S10,S12,S15,S16.
- Code or proof example: `python scripts/build-plugin-zip.py 1.69.x` and `python scripts/verify-plugin-release.py 1.69.x`
- Expected false-claim risk: I may trust a claimed ZIP instead of verifying the actual artifact.
- How you catch it: Catch by running verifier, checking ZIP entries and checking six version surfaces.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 541. Live Deploy and Recovery
- Action: Upload only the verified ZIP.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 542. Live Deploy and Recovery
- Action: Check plugin activation state.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 543. Live Deploy and Recovery
- Action: Check healthcheck version.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 544. Live Deploy and Recovery
- Action: Check project routes return 200.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 545. Live Deploy and Recovery
- Action: Flush permalinks only if routes are broken.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 546. Live Deploy and Recovery
- Action: Upload only the verified ZIP.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 547. Live Deploy and Recovery
- Action: Check plugin activation state.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 548. Live Deploy and Recovery
- Action: Check healthcheck version.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 549. Live Deploy and Recovery
- Action: Check project routes return 200.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 550. Live Deploy and Recovery
- Action: Flush permalinks only if routes are broken.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 551. Live Deploy and Recovery
- Action: Upload only the verified ZIP.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 552. Live Deploy and Recovery
- Action: Check plugin activation state.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 553. Live Deploy and Recovery
- Action: Check healthcheck version.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 554. Live Deploy and Recovery
- Action: Check project routes return 200.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 555. Live Deploy and Recovery
- Action: Flush permalinks only if routes are broken.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 556. Live Deploy and Recovery
- Action: Upload only the verified ZIP.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 557. Live Deploy and Recovery
- Action: Check plugin activation state.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 558. Live Deploy and Recovery
- Action: Check healthcheck version.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 559. Live Deploy and Recovery
- Action: Check project routes return 200.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 560. Live Deploy and Recovery
- Action: Flush permalinks only if routes are broken.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 561. Live Deploy and Recovery
- Action: Upload only the verified ZIP.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 562. Live Deploy and Recovery
- Action: Check plugin activation state.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 563. Live Deploy and Recovery
- Action: Check healthcheck version.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 564. Live Deploy and Recovery
- Action: Check project routes return 200.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 565. Live Deploy and Recovery
- Action: Flush permalinks only if routes are broken.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 566. Live Deploy and Recovery
- Action: Upload only the verified ZIP.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 567. Live Deploy and Recovery
- Action: Check plugin activation state.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 568. Live Deploy and Recovery
- Action: Check healthcheck version.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 569. Live Deploy and Recovery
- Action: Check project routes return 200.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 570. Live Deploy and Recovery
- Action: Flush permalinks only if routes are broken.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 571. Live Deploy and Recovery
- Action: Upload only the verified ZIP.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 572. Live Deploy and Recovery
- Action: Check plugin activation state.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 573. Live Deploy and Recovery
- Action: Check healthcheck version.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 574. Live Deploy and Recovery
- Action: Check project routes return 200.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 575. Live Deploy and Recovery
- Action: Flush permalinks only if routes are broken.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 576. Live Deploy and Recovery
- Action: Upload only the verified ZIP.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 577. Live Deploy and Recovery
- Action: Check plugin activation state.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 578. Live Deploy and Recovery
- Action: Check healthcheck version.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 579. Live Deploy and Recovery
- Action: Check project routes return 200.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 580. Live Deploy and Recovery
- Action: Flush permalinks only if routes are broken.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 581. Live Deploy and Recovery
- Action: Upload only the verified ZIP.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 582. Live Deploy and Recovery
- Action: Check plugin activation state.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 583. Live Deploy and Recovery
- Action: Check healthcheck version.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 584. Live Deploy and Recovery
- Action: Check project routes return 200.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 585. Live Deploy and Recovery
- Action: Flush permalinks only if routes are broken.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 586. Live Deploy and Recovery
- Action: Upload only the verified ZIP.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 587. Live Deploy and Recovery
- Action: Check plugin activation state.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 588. Live Deploy and Recovery
- Action: Check healthcheck version.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 589. Live Deploy and Recovery
- Action: Check project routes return 200.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 590. Live Deploy and Recovery
- Action: Flush permalinks only if routes are broken.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 591. Live Deploy and Recovery
- Action: Upload only the verified ZIP.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 592. Live Deploy and Recovery
- Action: Check plugin activation state.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 593. Live Deploy and Recovery
- Action: Check healthcheck version.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 594. Live Deploy and Recovery
- Action: Check project routes return 200.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 595. Live Deploy and Recovery
- Action: Flush permalinks only if routes are broken.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 596. Live Deploy and Recovery
- Action: Upload only the verified ZIP.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 597. Live Deploy and Recovery
- Action: Check plugin activation state.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 598. Live Deploy and Recovery
- Action: Check healthcheck version.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 599. Live Deploy and Recovery
- Action: Check project routes return 200.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 600. Live Deploy and Recovery
- Action: Flush permalinks only if routes are broken.
- Research proof set: S10,S12,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may confuse local success with live WordPress success.
- How you catch it: Catch by healthcheck, public URL status and fresh browser screenshots after deploy.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 601. Projects Archive Premium Shelf
- Action: Compare projects reference to current /projects/.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 602. Projects Archive Premium Shelf
- Action: Replace one old card surface with premium card pattern.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 603. Projects Archive Premium Shelf
- Action: Keep project facts real.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 604. Projects Archive Premium Shelf
- Action: Remove internal ranking labels.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 605. Projects Archive Premium Shelf
- Action: Screenshot desktop and mobile archive.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 606. Projects Archive Premium Shelf
- Action: Compare projects reference to current /projects/.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 607. Projects Archive Premium Shelf
- Action: Replace one old card surface with premium card pattern.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 608. Projects Archive Premium Shelf
- Action: Keep project facts real.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 609. Projects Archive Premium Shelf
- Action: Remove internal ranking labels.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 610. Projects Archive Premium Shelf
- Action: Screenshot desktop and mobile archive.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 611. Projects Archive Premium Shelf
- Action: Compare projects reference to current /projects/.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 612. Projects Archive Premium Shelf
- Action: Replace one old card surface with premium card pattern.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 613. Projects Archive Premium Shelf
- Action: Keep project facts real.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 614. Projects Archive Premium Shelf
- Action: Remove internal ranking labels.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 615. Projects Archive Premium Shelf
- Action: Screenshot desktop and mobile archive.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 616. Projects Archive Premium Shelf
- Action: Compare projects reference to current /projects/.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 617. Projects Archive Premium Shelf
- Action: Replace one old card surface with premium card pattern.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 618. Projects Archive Premium Shelf
- Action: Keep project facts real.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 619. Projects Archive Premium Shelf
- Action: Remove internal ranking labels.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 620. Projects Archive Premium Shelf
- Action: Screenshot desktop and mobile archive.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 621. Projects Archive Premium Shelf
- Action: Compare projects reference to current /projects/.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 622. Projects Archive Premium Shelf
- Action: Replace one old card surface with premium card pattern.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 623. Projects Archive Premium Shelf
- Action: Keep project facts real.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 624. Projects Archive Premium Shelf
- Action: Remove internal ranking labels.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 625. Projects Archive Premium Shelf
- Action: Screenshot desktop and mobile archive.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 626. Projects Archive Premium Shelf
- Action: Compare projects reference to current /projects/.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 627. Projects Archive Premium Shelf
- Action: Replace one old card surface with premium card pattern.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 628. Projects Archive Premium Shelf
- Action: Keep project facts real.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 629. Projects Archive Premium Shelf
- Action: Remove internal ranking labels.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 630. Projects Archive Premium Shelf
- Action: Screenshot desktop and mobile archive.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 631. Projects Archive Premium Shelf
- Action: Compare projects reference to current /projects/.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 632. Projects Archive Premium Shelf
- Action: Replace one old card surface with premium card pattern.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 633. Projects Archive Premium Shelf
- Action: Keep project facts real.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 634. Projects Archive Premium Shelf
- Action: Remove internal ranking labels.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 635. Projects Archive Premium Shelf
- Action: Screenshot desktop and mobile archive.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 636. Projects Archive Premium Shelf
- Action: Compare projects reference to current /projects/.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 637. Projects Archive Premium Shelf
- Action: Replace one old card surface with premium card pattern.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 638. Projects Archive Premium Shelf
- Action: Keep project facts real.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 639. Projects Archive Premium Shelf
- Action: Remove internal ranking labels.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 640. Projects Archive Premium Shelf
- Action: Screenshot desktop and mobile archive.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 641. Projects Archive Premium Shelf
- Action: Compare projects reference to current /projects/.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 642. Projects Archive Premium Shelf
- Action: Replace one old card surface with premium card pattern.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 643. Projects Archive Premium Shelf
- Action: Keep project facts real.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 644. Projects Archive Premium Shelf
- Action: Remove internal ranking labels.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 645. Projects Archive Premium Shelf
- Action: Screenshot desktop and mobile archive.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 646. Projects Archive Premium Shelf
- Action: Compare projects reference to current /projects/.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 647. Projects Archive Premium Shelf
- Action: Replace one old card surface with premium card pattern.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 648. Projects Archive Premium Shelf
- Action: Keep project facts real.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 649. Projects Archive Premium Shelf
- Action: Remove internal ranking labels.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 650. Projects Archive Premium Shelf
- Action: Screenshot desktop and mobile archive.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 651. Projects Archive Premium Shelf
- Action: Compare projects reference to current /projects/.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 652. Projects Archive Premium Shelf
- Action: Replace one old card surface with premium card pattern.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 653. Projects Archive Premium Shelf
- Action: Keep project facts real.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 654. Projects Archive Premium Shelf
- Action: Remove internal ranking labels.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 655. Projects Archive Premium Shelf
- Action: Screenshot desktop and mobile archive.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 656. Projects Archive Premium Shelf
- Action: Compare projects reference to current /projects/.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 657. Projects Archive Premium Shelf
- Action: Replace one old card surface with premium card pattern.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 658. Projects Archive Premium Shelf
- Action: Keep project facts real.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 659. Projects Archive Premium Shelf
- Action: Remove internal ranking labels.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 660. Projects Archive Premium Shelf
- Action: Screenshot desktop and mobile archive.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 661. Homepage Premium Brand Shell
- Action: Compare homepage reference to live homepage.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 662. Homepage Premium Brand Shell
- Action: Implement one first-viewport brand element.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 663. Homepage Premium Brand Shell
- Action: Connect one project card to showroom path.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 664. Homepage Premium Brand Shell
- Action: Keep buyer and developer paths clear.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 665. Homepage Premium Brand Shell
- Action: Screenshot first viewport and below fold.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 666. Homepage Premium Brand Shell
- Action: Compare homepage reference to live homepage.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 667. Homepage Premium Brand Shell
- Action: Implement one first-viewport brand element.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 668. Homepage Premium Brand Shell
- Action: Connect one project card to showroom path.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 669. Homepage Premium Brand Shell
- Action: Keep buyer and developer paths clear.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 670. Homepage Premium Brand Shell
- Action: Screenshot first viewport and below fold.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 671. Homepage Premium Brand Shell
- Action: Compare homepage reference to live homepage.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 672. Homepage Premium Brand Shell
- Action: Implement one first-viewport brand element.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 673. Homepage Premium Brand Shell
- Action: Connect one project card to showroom path.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 674. Homepage Premium Brand Shell
- Action: Keep buyer and developer paths clear.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 675. Homepage Premium Brand Shell
- Action: Screenshot first viewport and below fold.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 676. Homepage Premium Brand Shell
- Action: Compare homepage reference to live homepage.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 677. Homepage Premium Brand Shell
- Action: Implement one first-viewport brand element.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 678. Homepage Premium Brand Shell
- Action: Connect one project card to showroom path.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 679. Homepage Premium Brand Shell
- Action: Keep buyer and developer paths clear.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 680. Homepage Premium Brand Shell
- Action: Screenshot first viewport and below fold.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 681. Homepage Premium Brand Shell
- Action: Compare homepage reference to live homepage.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 682. Homepage Premium Brand Shell
- Action: Implement one first-viewport brand element.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 683. Homepage Premium Brand Shell
- Action: Connect one project card to showroom path.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 684. Homepage Premium Brand Shell
- Action: Keep buyer and developer paths clear.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 685. Homepage Premium Brand Shell
- Action: Screenshot first viewport and below fold.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 686. Homepage Premium Brand Shell
- Action: Compare homepage reference to live homepage.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 687. Homepage Premium Brand Shell
- Action: Implement one first-viewport brand element.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 688. Homepage Premium Brand Shell
- Action: Connect one project card to showroom path.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 689. Homepage Premium Brand Shell
- Action: Keep buyer and developer paths clear.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 690. Homepage Premium Brand Shell
- Action: Screenshot first viewport and below fold.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 691. Homepage Premium Brand Shell
- Action: Compare homepage reference to live homepage.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 692. Homepage Premium Brand Shell
- Action: Implement one first-viewport brand element.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 693. Homepage Premium Brand Shell
- Action: Connect one project card to showroom path.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 694. Homepage Premium Brand Shell
- Action: Keep buyer and developer paths clear.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 695. Homepage Premium Brand Shell
- Action: Screenshot first viewport and below fold.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 696. Homepage Premium Brand Shell
- Action: Compare homepage reference to live homepage.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 697. Homepage Premium Brand Shell
- Action: Implement one first-viewport brand element.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 698. Homepage Premium Brand Shell
- Action: Connect one project card to showroom path.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 699. Homepage Premium Brand Shell
- Action: Keep buyer and developer paths clear.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 700. Homepage Premium Brand Shell
- Action: Screenshot first viewport and below fold.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 701. Homepage Premium Brand Shell
- Action: Compare homepage reference to live homepage.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 702. Homepage Premium Brand Shell
- Action: Implement one first-viewport brand element.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 703. Homepage Premium Brand Shell
- Action: Connect one project card to showroom path.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 704. Homepage Premium Brand Shell
- Action: Keep buyer and developer paths clear.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 705. Homepage Premium Brand Shell
- Action: Screenshot first viewport and below fold.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 706. Homepage Premium Brand Shell
- Action: Compare homepage reference to live homepage.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 707. Homepage Premium Brand Shell
- Action: Implement one first-viewport brand element.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 708. Homepage Premium Brand Shell
- Action: Connect one project card to showroom path.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 709. Homepage Premium Brand Shell
- Action: Keep buyer and developer paths clear.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 710. Homepage Premium Brand Shell
- Action: Screenshot first viewport and below fold.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 711. Homepage Premium Brand Shell
- Action: Compare homepage reference to live homepage.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 712. Homepage Premium Brand Shell
- Action: Implement one first-viewport brand element.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 713. Homepage Premium Brand Shell
- Action: Connect one project card to showroom path.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 714. Homepage Premium Brand Shell
- Action: Keep buyer and developer paths clear.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 715. Homepage Premium Brand Shell
- Action: Screenshot first viewport and below fold.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 716. Homepage Premium Brand Shell
- Action: Compare homepage reference to live homepage.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 717. Homepage Premium Brand Shell
- Action: Implement one first-viewport brand element.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 718. Homepage Premium Brand Shell
- Action: Connect one project card to showroom path.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 719. Homepage Premium Brand Shell
- Action: Keep buyer and developer paths clear.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 720. Homepage Premium Brand Shell
- Action: Screenshot first viewport and below fold.
- Research proof set: S03,S05,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 721. Brand Assets and Favicon
- Action: Copy one Lovable brand asset to the correct theme/plugin asset path.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 722. Brand Assets and Favicon
- Action: Wire one favicon link.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 723. Brand Assets and Favicon
- Action: Verify browser tab or page source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 724. Brand Assets and Favicon
- Action: Wire one OG image source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 725. Brand Assets and Favicon
- Action: Check image size and sharpness.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 726. Brand Assets and Favicon
- Action: Copy one Lovable brand asset to the correct theme/plugin asset path.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 727. Brand Assets and Favicon
- Action: Wire one favicon link.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 728. Brand Assets and Favicon
- Action: Verify browser tab or page source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 729. Brand Assets and Favicon
- Action: Wire one OG image source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 730. Brand Assets and Favicon
- Action: Check image size and sharpness.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 731. Brand Assets and Favicon
- Action: Copy one Lovable brand asset to the correct theme/plugin asset path.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 732. Brand Assets and Favicon
- Action: Wire one favicon link.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 733. Brand Assets and Favicon
- Action: Verify browser tab or page source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 734. Brand Assets and Favicon
- Action: Wire one OG image source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 735. Brand Assets and Favicon
- Action: Check image size and sharpness.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 736. Brand Assets and Favicon
- Action: Copy one Lovable brand asset to the correct theme/plugin asset path.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 737. Brand Assets and Favicon
- Action: Wire one favicon link.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 738. Brand Assets and Favicon
- Action: Verify browser tab or page source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 739. Brand Assets and Favicon
- Action: Wire one OG image source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 740. Brand Assets and Favicon
- Action: Check image size and sharpness.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 741. Brand Assets and Favicon
- Action: Copy one Lovable brand asset to the correct theme/plugin asset path.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 742. Brand Assets and Favicon
- Action: Wire one favicon link.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 743. Brand Assets and Favicon
- Action: Verify browser tab or page source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 744. Brand Assets and Favicon
- Action: Wire one OG image source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 745. Brand Assets and Favicon
- Action: Check image size and sharpness.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 746. Brand Assets and Favicon
- Action: Copy one Lovable brand asset to the correct theme/plugin asset path.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 747. Brand Assets and Favicon
- Action: Wire one favicon link.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 748. Brand Assets and Favicon
- Action: Verify browser tab or page source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 749. Brand Assets and Favicon
- Action: Wire one OG image source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 750. Brand Assets and Favicon
- Action: Check image size and sharpness.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 751. Brand Assets and Favicon
- Action: Copy one Lovable brand asset to the correct theme/plugin asset path.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 752. Brand Assets and Favicon
- Action: Wire one favicon link.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 753. Brand Assets and Favicon
- Action: Verify browser tab or page source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 754. Brand Assets and Favicon
- Action: Wire one OG image source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 755. Brand Assets and Favicon
- Action: Check image size and sharpness.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 756. Brand Assets and Favicon
- Action: Copy one Lovable brand asset to the correct theme/plugin asset path.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 757. Brand Assets and Favicon
- Action: Wire one favicon link.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 758. Brand Assets and Favicon
- Action: Verify browser tab or page source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 759. Brand Assets and Favicon
- Action: Wire one OG image source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 760. Brand Assets and Favicon
- Action: Check image size and sharpness.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 761. Brand Assets and Favicon
- Action: Copy one Lovable brand asset to the correct theme/plugin asset path.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 762. Brand Assets and Favicon
- Action: Wire one favicon link.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 763. Brand Assets and Favicon
- Action: Verify browser tab or page source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 764. Brand Assets and Favicon
- Action: Wire one OG image source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 765. Brand Assets and Favicon
- Action: Check image size and sharpness.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 766. Brand Assets and Favicon
- Action: Copy one Lovable brand asset to the correct theme/plugin asset path.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 767. Brand Assets and Favicon
- Action: Wire one favicon link.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 768. Brand Assets and Favicon
- Action: Verify browser tab or page source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 769. Brand Assets and Favicon
- Action: Wire one OG image source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 770. Brand Assets and Favicon
- Action: Check image size and sharpness.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 771. Brand Assets and Favicon
- Action: Copy one Lovable brand asset to the correct theme/plugin asset path.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 772. Brand Assets and Favicon
- Action: Wire one favicon link.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 773. Brand Assets and Favicon
- Action: Verify browser tab or page source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 774. Brand Assets and Favicon
- Action: Wire one OG image source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 775. Brand Assets and Favicon
- Action: Check image size and sharpness.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 776. Brand Assets and Favicon
- Action: Copy one Lovable brand asset to the correct theme/plugin asset path.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 777. Brand Assets and Favicon
- Action: Wire one favicon link.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 778. Brand Assets and Favicon
- Action: Verify browser tab or page source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 779. Brand Assets and Favicon
- Action: Wire one OG image source.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 780. Brand Assets and Favicon
- Action: Check image size and sharpness.
- Research proof set: S02,S06,S13,S17.
- Code or proof example: `<link rel="icon" sizes="32x32" href=".../favicon-32.png">`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 781. SEO and Structured Data
- Action: Assign one canonical intent to one page.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 782. SEO and Structured Data
- Action: Check one internal link target.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 783. SEO and Structured Data
- Action: Ensure schema matches visible content.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 784. SEO and Structured Data
- Action: Prevent one cannibalizing title pattern.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 785. SEO and Structured Data
- Action: Record one page in the canonical registry.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 786. SEO and Structured Data
- Action: Assign one canonical intent to one page.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 787. SEO and Structured Data
- Action: Check one internal link target.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 788. SEO and Structured Data
- Action: Ensure schema matches visible content.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 789. SEO and Structured Data
- Action: Prevent one cannibalizing title pattern.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 790. SEO and Structured Data
- Action: Record one page in the canonical registry.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 791. SEO and Structured Data
- Action: Assign one canonical intent to one page.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 792. SEO and Structured Data
- Action: Check one internal link target.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 793. SEO and Structured Data
- Action: Ensure schema matches visible content.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 794. SEO and Structured Data
- Action: Prevent one cannibalizing title pattern.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 795. SEO and Structured Data
- Action: Record one page in the canonical registry.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 796. SEO and Structured Data
- Action: Assign one canonical intent to one page.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 797. SEO and Structured Data
- Action: Check one internal link target.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 798. SEO and Structured Data
- Action: Ensure schema matches visible content.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 799. SEO and Structured Data
- Action: Prevent one cannibalizing title pattern.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 800. SEO and Structured Data
- Action: Record one page in the canonical registry.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 801. SEO and Structured Data
- Action: Assign one canonical intent to one page.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 802. SEO and Structured Data
- Action: Check one internal link target.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 803. SEO and Structured Data
- Action: Ensure schema matches visible content.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 804. SEO and Structured Data
- Action: Prevent one cannibalizing title pattern.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 805. SEO and Structured Data
- Action: Record one page in the canonical registry.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 806. SEO and Structured Data
- Action: Assign one canonical intent to one page.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 807. SEO and Structured Data
- Action: Check one internal link target.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 808. SEO and Structured Data
- Action: Ensure schema matches visible content.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 809. SEO and Structured Data
- Action: Prevent one cannibalizing title pattern.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 810. SEO and Structured Data
- Action: Record one page in the canonical registry.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 811. SEO and Structured Data
- Action: Assign one canonical intent to one page.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 812. SEO and Structured Data
- Action: Check one internal link target.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 813. SEO and Structured Data
- Action: Ensure schema matches visible content.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 814. SEO and Structured Data
- Action: Prevent one cannibalizing title pattern.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 815. SEO and Structured Data
- Action: Record one page in the canonical registry.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 816. SEO and Structured Data
- Action: Assign one canonical intent to one page.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 817. SEO and Structured Data
- Action: Check one internal link target.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 818. SEO and Structured Data
- Action: Ensure schema matches visible content.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 819. SEO and Structured Data
- Action: Prevent one cannibalizing title pattern.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 820. SEO and Structured Data
- Action: Record one page in the canonical registry.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 821. SEO and Structured Data
- Action: Assign one canonical intent to one page.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 822. SEO and Structured Data
- Action: Check one internal link target.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 823. SEO and Structured Data
- Action: Ensure schema matches visible content.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 824. SEO and Structured Data
- Action: Prevent one cannibalizing title pattern.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 825. SEO and Structured Data
- Action: Record one page in the canonical registry.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 826. SEO and Structured Data
- Action: Assign one canonical intent to one page.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 827. SEO and Structured Data
- Action: Check one internal link target.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 828. SEO and Structured Data
- Action: Ensure schema matches visible content.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 829. SEO and Structured Data
- Action: Prevent one cannibalizing title pattern.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 830. SEO and Structured Data
- Action: Record one page in the canonical registry.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 831. SEO and Structured Data
- Action: Assign one canonical intent to one page.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 832. SEO and Structured Data
- Action: Check one internal link target.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 833. SEO and Structured Data
- Action: Ensure schema matches visible content.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 834. SEO and Structured Data
- Action: Prevent one cannibalizing title pattern.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 835. SEO and Structured Data
- Action: Record one page in the canonical registry.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 836. SEO and Structured Data
- Action: Assign one canonical intent to one page.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 837. SEO and Structured Data
- Action: Check one internal link target.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 838. SEO and Structured Data
- Action: Ensure schema matches visible content.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 839. SEO and Structured Data
- Action: Prevent one cannibalizing title pattern.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 840. SEO and Structured Data
- Action: Record one page in the canonical registry.
- Research proof set: S14,S16,S17.
- Code or proof example: `Project page links to city hub; support guide links to canonical money page; no competing title intent.`
- Expected false-claim risk: I may create another page that competes with an existing money page.
- How you catch it: Catch by canonical registry and internal-link target review.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 841. Admin War Room
- Action: Define one admin-only view.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 842. Admin War Room
- Action: Gate one admin output by capability.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 843. Admin War Room
- Action: Render one report in readable RTL format.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 844. Admin War Room
- Action: Show one source commit and date.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 845. Admin War Room
- Action: Keep strategy language private.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 846. Admin War Room
- Action: Define one admin-only view.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 847. Admin War Room
- Action: Gate one admin output by capability.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 848. Admin War Room
- Action: Render one report in readable RTL format.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 849. Admin War Room
- Action: Show one source commit and date.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 850. Admin War Room
- Action: Keep strategy language private.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 851. Admin War Room
- Action: Define one admin-only view.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 852. Admin War Room
- Action: Gate one admin output by capability.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 853. Admin War Room
- Action: Render one report in readable RTL format.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 854. Admin War Room
- Action: Show one source commit and date.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 855. Admin War Room
- Action: Keep strategy language private.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 856. Admin War Room
- Action: Define one admin-only view.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 857. Admin War Room
- Action: Gate one admin output by capability.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 858. Admin War Room
- Action: Render one report in readable RTL format.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 859. Admin War Room
- Action: Show one source commit and date.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 860. Admin War Room
- Action: Keep strategy language private.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 861. Admin War Room
- Action: Define one admin-only view.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 862. Admin War Room
- Action: Gate one admin output by capability.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 863. Admin War Room
- Action: Render one report in readable RTL format.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 864. Admin War Room
- Action: Show one source commit and date.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 865. Admin War Room
- Action: Keep strategy language private.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 866. Admin War Room
- Action: Define one admin-only view.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 867. Admin War Room
- Action: Gate one admin output by capability.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 868. Admin War Room
- Action: Render one report in readable RTL format.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 869. Admin War Room
- Action: Show one source commit and date.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 870. Admin War Room
- Action: Keep strategy language private.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 871. Admin War Room
- Action: Define one admin-only view.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 872. Admin War Room
- Action: Gate one admin output by capability.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 873. Admin War Room
- Action: Render one report in readable RTL format.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 874. Admin War Room
- Action: Show one source commit and date.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 875. Admin War Room
- Action: Keep strategy language private.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 876. Admin War Room
- Action: Define one admin-only view.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 877. Admin War Room
- Action: Gate one admin output by capability.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 878. Admin War Room
- Action: Render one report in readable RTL format.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 879. Admin War Room
- Action: Show one source commit and date.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 880. Admin War Room
- Action: Keep strategy language private.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 881. Admin War Room
- Action: Define one admin-only view.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 882. Admin War Room
- Action: Gate one admin output by capability.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 883. Admin War Room
- Action: Render one report in readable RTL format.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 884. Admin War Room
- Action: Show one source commit and date.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 885. Admin War Room
- Action: Keep strategy language private.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 886. Admin War Room
- Action: Define one admin-only view.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 887. Admin War Room
- Action: Gate one admin output by capability.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 888. Admin War Room
- Action: Render one report in readable RTL format.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 889. Admin War Room
- Action: Show one source commit and date.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 890. Admin War Room
- Action: Keep strategy language private.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 891. Admin War Room
- Action: Define one admin-only view.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 892. Admin War Room
- Action: Gate one admin output by capability.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 893. Admin War Room
- Action: Render one report in readable RTL format.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 894. Admin War Room
- Action: Show one source commit and date.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 895. Admin War Room
- Action: Keep strategy language private.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 896. Admin War Room
- Action: Define one admin-only view.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 897. Admin War Room
- Action: Gate one admin output by capability.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 898. Admin War Room
- Action: Render one report in readable RTL format.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 899. Admin War Room
- Action: Show one source commit and date.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 900. Admin War Room
- Action: Keep strategy language private.
- Research proof set: S10,S11,S16.
- Code or proof example: `current_user_can('manage_options')` gate before strategy-room output.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 901. Skills and Process Capture
- Action: Add one learned rule to the master skill.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 902. Skills and Process Capture
- Action: Update one shared skill without deleting old skills.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 903. Skills and Process Capture
- Action: Record one failure and the catch mechanism.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 904. Skills and Process Capture
- Action: Link one proof folder to the skill.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 905. Skills and Process Capture
- Action: Add one next-run checkpoint.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 906. Skills and Process Capture
- Action: Add one learned rule to the master skill.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 907. Skills and Process Capture
- Action: Update one shared skill without deleting old skills.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 908. Skills and Process Capture
- Action: Record one failure and the catch mechanism.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 909. Skills and Process Capture
- Action: Link one proof folder to the skill.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 910. Skills and Process Capture
- Action: Add one next-run checkpoint.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 911. Skills and Process Capture
- Action: Add one learned rule to the master skill.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 912. Skills and Process Capture
- Action: Update one shared skill without deleting old skills.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 913. Skills and Process Capture
- Action: Record one failure and the catch mechanism.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 914. Skills and Process Capture
- Action: Link one proof folder to the skill.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 915. Skills and Process Capture
- Action: Add one next-run checkpoint.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 916. Skills and Process Capture
- Action: Add one learned rule to the master skill.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 917. Skills and Process Capture
- Action: Update one shared skill without deleting old skills.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 918. Skills and Process Capture
- Action: Record one failure and the catch mechanism.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 919. Skills and Process Capture
- Action: Link one proof folder to the skill.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 920. Skills and Process Capture
- Action: Add one next-run checkpoint.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 921. Skills and Process Capture
- Action: Add one learned rule to the master skill.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 922. Skills and Process Capture
- Action: Update one shared skill without deleting old skills.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 923. Skills and Process Capture
- Action: Record one failure and the catch mechanism.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 924. Skills and Process Capture
- Action: Link one proof folder to the skill.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 925. Skills and Process Capture
- Action: Add one next-run checkpoint.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 926. Skills and Process Capture
- Action: Add one learned rule to the master skill.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 927. Skills and Process Capture
- Action: Update one shared skill without deleting old skills.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 928. Skills and Process Capture
- Action: Record one failure and the catch mechanism.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 929. Skills and Process Capture
- Action: Link one proof folder to the skill.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 930. Skills and Process Capture
- Action: Add one next-run checkpoint.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 931. Skills and Process Capture
- Action: Add one learned rule to the master skill.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 932. Skills and Process Capture
- Action: Update one shared skill without deleting old skills.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 933. Skills and Process Capture
- Action: Record one failure and the catch mechanism.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 934. Skills and Process Capture
- Action: Link one proof folder to the skill.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 935. Skills and Process Capture
- Action: Add one next-run checkpoint.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 936. Skills and Process Capture
- Action: Add one learned rule to the master skill.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 937. Skills and Process Capture
- Action: Update one shared skill without deleting old skills.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 938. Skills and Process Capture
- Action: Record one failure and the catch mechanism.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 939. Skills and Process Capture
- Action: Link one proof folder to the skill.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 940. Skills and Process Capture
- Action: Add one next-run checkpoint.
- Research proof set: S15,S16.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 941. Full QA Gallery
- Action: Capture one required state screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 942. Full QA Gallery
- Action: Save one screenshot into docs/qa/screenshots.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 943. Full QA Gallery
- Action: Write one JSON proof field.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 944. Full QA Gallery
- Action: Inspect one screenshot for visual mismatch.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 945. Full QA Gallery
- Action: Mark one limitation honestly.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 946. Full QA Gallery
- Action: Capture one required state screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 947. Full QA Gallery
- Action: Save one screenshot into docs/qa/screenshots.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 948. Full QA Gallery
- Action: Write one JSON proof field.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 949. Full QA Gallery
- Action: Inspect one screenshot for visual mismatch.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 950. Full QA Gallery
- Action: Mark one limitation honestly.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 951. Full QA Gallery
- Action: Capture one required state screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 952. Full QA Gallery
- Action: Save one screenshot into docs/qa/screenshots.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 953. Full QA Gallery
- Action: Write one JSON proof field.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 954. Full QA Gallery
- Action: Inspect one screenshot for visual mismatch.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 955. Full QA Gallery
- Action: Mark one limitation honestly.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 956. Full QA Gallery
- Action: Capture one required state screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 957. Full QA Gallery
- Action: Save one screenshot into docs/qa/screenshots.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 958. Full QA Gallery
- Action: Write one JSON proof field.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 959. Full QA Gallery
- Action: Inspect one screenshot for visual mismatch.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 960. Full QA Gallery
- Action: Mark one limitation honestly.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 961. Full QA Gallery
- Action: Capture one required state screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 962. Full QA Gallery
- Action: Save one screenshot into docs/qa/screenshots.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 963. Full QA Gallery
- Action: Write one JSON proof field.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 964. Full QA Gallery
- Action: Inspect one screenshot for visual mismatch.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 965. Full QA Gallery
- Action: Mark one limitation honestly.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 966. Full QA Gallery
- Action: Capture one required state screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 967. Full QA Gallery
- Action: Save one screenshot into docs/qa/screenshots.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 968. Full QA Gallery
- Action: Write one JSON proof field.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 969. Full QA Gallery
- Action: Inspect one screenshot for visual mismatch.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 970. Full QA Gallery
- Action: Mark one limitation honestly.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 971. Full QA Gallery
- Action: Capture one required state screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 972. Full QA Gallery
- Action: Save one screenshot into docs/qa/screenshots.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 973. Full QA Gallery
- Action: Write one JSON proof field.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 974. Full QA Gallery
- Action: Inspect one screenshot for visual mismatch.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 975. Full QA Gallery
- Action: Mark one limitation honestly.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 976. Full QA Gallery
- Action: Capture one required state screenshot.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 977. Full QA Gallery
- Action: Save one screenshot into docs/qa/screenshots.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 978. Full QA Gallery
- Action: Write one JSON proof field.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 979. Full QA Gallery
- Action: Inspect one screenshot for visual mismatch.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 980. Full QA Gallery
- Action: Mark one limitation honestly.
- Research proof set: S06,S07,S13,S16.
- Code or proof example: `document.documentElement.scrollWidth === window.innerWidth`
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 981. Owner Demo Readiness
- Action: Assemble one showable owner path.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 982. Owner Demo Readiness
- Action: Write one honest limitation.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 983. Owner Demo Readiness
- Action: Write one rollback step.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 984. Owner Demo Readiness
- Action: List one missing contractor asset.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 985. Owner Demo Readiness
- Action: Confirm the final demo page is not patched-looking.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 986. Owner Demo Readiness
- Action: Assemble one showable owner path.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 987. Owner Demo Readiness
- Action: Write one honest limitation.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 988. Owner Demo Readiness
- Action: Write one rollback step.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 989. Owner Demo Readiness
- Action: List one missing contractor asset.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 990. Owner Demo Readiness
- Action: Confirm the final demo page is not patched-looking.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 991. Owner Demo Readiness
- Action: Assemble one showable owner path.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 992. Owner Demo Readiness
- Action: Write one honest limitation.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 993. Owner Demo Readiness
- Action: Write one rollback step.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 994. Owner Demo Readiness
- Action: List one missing contractor asset.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 995. Owner Demo Readiness
- Action: Confirm the final demo page is not patched-looking.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 996. Owner Demo Readiness
- Action: Assemble one showable owner path.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 997. Owner Demo Readiness
- Action: Write one honest limitation.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 998. Owner Demo Readiness
- Action: Write one rollback step.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 999. Owner Demo Readiness
- Action: List one missing contractor asset.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

### 1000. Owner Demo Readiness
- Action: Confirm the final demo page is not patched-looking.
- Research proof set: S16,S17,S18.
- Code or proof example: `git status`, screenshot, source file path, version, and proof file must agree.
- Expected false-claim risk: I may claim a file, screenshot or behavior exists without a direct proof path.
- How you catch it: Catch by opening the exact repo path, exact GitHub URL, exact screenshot and exact command output.
- Required fix if caught: stop, write the mismatch, remove the wrong active source or false claim, rerun the proof, and only then continue.

