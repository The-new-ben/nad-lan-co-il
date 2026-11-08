# Property fact lookup review

Reviewed on 8 November 2026 against the confirmed Kochav HaTzafon brief and the fresh page 7812 snapshot in `research/primary/kochav-confirmed/`. This is an editorial answer lookup, not language model inference. No model, browser, server restart or public deployment was performed for this review.

## Findings and routing correction

The advertised price, approximate areas, amenities, incomplete condominium registration and the absence of a verified investment return are substantially supported by the saved listing. The original routing could nevertheless attach those facts to the wrong subject. The retained before-change evidence is `evidence/property-context-review.json`.

- An earlier property discussion caused a Rehovot apartment question to receive the eighteen-million-shekel answer. A lone “Kochav,” another Meital Katzir listing in Sde Dov and neighborhood-wide housing questions also received that figure. The revised lookup requires the full neighborhood identity plus a singular listing reference. It accepts only recognized follow-up wording and stops context inheritance at an ambiguous intervening turn. Unrecognized place/property words, indefinite homes, comparisons and market/plural questions return `None` without a geographic blacklist.
- Purchase tax and bridge construction cost were mistaken for the asking price. Tax, mortgage, rental, payment and cost questions now leave this lookup. Asking-price intent requires the word “price”; generic “how much” no longer establishes that intent.
- The source distinguishes the planned Rokach/Levi Eshkol route from the operating 180-metre Yarkon-to-Ibn-Gabirol bridge. Only an explicitly identified Rokach/Levi Eshkol bridge receives the existing planned-bridge answer. The other route and an unnamed bridge return `None`; this patch adds no new bridge assertion.
- Mixed identity or viewing requests could receive a fact answer while bypassing the intended role handling. Identity, broker and action language now takes precedence over fact intent and returns `None`.

`research/verify_property_context.py` checks the reproduced failures, new-place/history boundaries, bridge ambiguity, mixed identity/action questions and ordinary supported follow-ups. The resulting receipt is `evidence/property-context-regressions.json`. The lookup intentionally prefers declining a phrasing over guessing; `None` is a routing result, not a successful factual answer. The caller remains responsible for its general role/grounding behavior.

## Copy qualifications left for the owner's integration review

This authorized patch changes routing only. Existing `FACTS` and answer text remain unchanged.

- The primary listing labels approximately 197 sqm as **built area**. “Indoors” or “inside” is less precise and can imply net usable area. Prefer “advertised built area” when copy changes are authorized, retaining the approximate figure and plan/registration check.
- The overview and value replies emphasize positive features without the incomplete-registration qualification. The registration and area replies do contain it. The first substantive overview/value assessment should also make that material qualification visible under the confirmed brief.
- Five rooms is the advertised Israeli room count, not five bedrooms. No new bedroom count should be inferred.

## Source provenance

The supplied source receipt records 165,034 UTF-8 bytes and SHA-256 `432ea3759fa8f85d3962b0ad890468ebe218f7cfd12e4af73669a9782cb337f9`. The local HTML has Windows CRLF endings and 165,761 raw bytes. Reading as text and normalizing line endings to LF reproduces the receipt's bytes and hash exactly. Record that normalization explicitly, or retain an additional raw-file hash, rather than treating this as unexplained source drift.

Pilot scope remains page 5154. This review and local routing change do not authorize another public page, a live-market claim, or a claim that these prepared answers came from model inference.

Coordinator integration copy review: overview and value now mention incomplete condominium registration; the area reply and facts now say advertised built area rather than net indoors. Routing unchanged; all54 regression checks were rerun after the copy adjustment. No public property-answer integration yet.
