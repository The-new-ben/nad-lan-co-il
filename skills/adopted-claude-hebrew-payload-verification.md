# Adopted: Hebrew payload verification trap (Claude, 2026-08-13)

> A fix looked broken because the CHECK was broken. Verifying Hebrew values
> against raw page HTML fails silently: embedded JSON payloads store Hebrew
> as unicode escapes (`מ...`), so a plain-text needle returns "absent"
> even when the value is live.

## The incident

v1.72.197 shipped a per-project hero eyebrow. A raw-HTML check for the Hebrew
label reported it missing; one report went out calling the fix "still
resisting". Root cause: the value sat in the payload escaped. The rendered
hero (client-drawn) showed it correctly all along — proven by screenshot.

## The law

1. Hebrew/RTL values inside embedded JSON are verified with the ESCAPED
   needle: `json.dumps(value, ensure_ascii=True)[1:-1]` — or by key name
   (`"field":`), never by raw Hebrew text.
2. Client-rendered UI text is NEVER verifiable from raw HTML at all — the
   only proof is a real screenshot of the rendered page (visual proof loop).
3. When a fix "did not take", suspect the verification before re-fixing:
   re-deploying a working fix wastes a cycle and erodes owner trust.

## Related

- skills/adopted-codex-visual-proof-loop.md (screenshots are the only sight)
- The 2026-08-09 lesson: element-level checks must strip <style>/comments
  before counting h1/nlpf tokens (CSS text false-positives — same family).
