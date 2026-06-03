# docs/qa/ — QA session reports land here

Cowork writes one markdown file per QA session here, named
`QA-RUN-<YYYY-MM-DD>-<persona-slug>.md`, using the template in
[`skills/qa-journey-testing.md`](../../skills/qa-journey-testing.md) (PART D).

**The flow:**
1. Cowork runs a persona journey (charter + steps in the skill).
2. Cowork commits the report here + opens a PR `QA run <date> — <persona>`.
3. Claude (code) reads the report, fixes Blockers/Majors, ships a plugin version.
4. Owner updates + reviews.
5. Cowork re-runs → marks each bug FIXED / STILL-BROKEN / REGRESSED.

The acceptance bar for "ship-grade" is in the skill, PART E.

Persona slugs: `dana-buyer`, `yael-rainbow-advertiser`, `moshe-contractor`,
`avi-leadseeker`, `adversary`.
