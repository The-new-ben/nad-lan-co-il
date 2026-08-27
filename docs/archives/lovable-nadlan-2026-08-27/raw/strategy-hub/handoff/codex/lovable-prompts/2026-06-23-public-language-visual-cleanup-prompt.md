# Lovable Prompt - Public Language And Visual Cleanup

Paste into Lovable after it has synced `nadlan-strategy-hub/main` at commit `eaaba35` or later.

```text
You are working in the NadLan Strategy Hub repo.

Goal: do a focused public-language and visual-truth cleanup pass on the existing Nadlan3D prototype. Do not rebuild the concept from scratch.

Before editing, read:

1. handoff/shared-knowledge/skills/nadlan-screenshot-first-visual-qa.md
2. handoff/shared-knowledge/skills/nadlan-public-language-cleanup.md
3. handoff/lovable/2026-06-23-war-room-sync/reports/06-codex-visual-qa.md
4. handoff/lovable/2026-06-23-war-room-sync/source-manifest.md

Fix the public UI language:

- Remove internal words from public pages: GLB, SVG, RTL, 390px, font names, fallback, placeholder, mock, asset truth, Featured/Sponsored/Promoted taxonomy.
- Replace Showroom in Hebrew UI with natural buyer language such as "סיור בפרויקט", "תצוגת הפרויקט", or "סיור תלת-ממד".
- If paid placement disclosure is needed, use one public label such as "ממומן" or "מודעה" in Hebrew and "Ad" or "Sponsored" in English. Do not expose the internal ranking cascade.
- Replace technical value props like "Mobile first, RTL" and font names with buyer-facing copy or remove them.
- Keep transparency around illustrative plans, but say "תכנית להמחשה בלבד" / "Illustrative plan", not AI jargon.
- Remove em dashes from new public copy.
- Remove generic AI-sounding filler.

Fix visual truth:

- Do not present Rainbow as a live GLB unless the actual model file loads. If the model is missing, label it honestly as a 3D model pending upload or use a premium missing state.
- Do not use generic stock photos for important project cards when they look unrelated to the project.
- If no real project image exists, use a premium missing state or clearly labeled illustrative image.
- Dimri's facade fallback must not look like a final real facade. Either improve it from a source image or label it clearly as illustrative.

Fix known layout issue:

- The sticky WhatsApp/contact dock overlaps the footer on showroom pages. Add correct bottom spacing or make the dock stop before the footer.

Required screenshots after fixing:

- home HE mobile 390 and desktop 1440
- home EN mobile 390 and desktop 1440
- listings HE mobile 390 and desktop 1440
- listings EN mobile 390 and desktop 1440
- showroom Rainbow HE mobile 390 and desktop 1440
- showroom Rainbow EN mobile 390 and desktop 1440
- showroom Dimri HE mobile 390 and desktop 1440
- empty asset state HE mobile 390 and desktop 1440
- city Tel Aviv HE and EN, mobile 390 and desktop 1440
- mobile menu open in HE and EN

Save screenshots under:

handoff/lovable/2026-06-23-war-room-sync/screenshots/

Add a report:

handoff/lovable/2026-06-23-war-room-sync/reports/07-public-language-visual-cleanup.md

The report must list:

- internal terms removed
- replacement public labels
- image truth status for every visible project card
- remaining missing assets
- screenshots captured
- whether the result is contractor-sellable or still prototype-only

Do not claim completion without screenshots.
Commit and push to main.
Return the commit hash and changed file list.
```

