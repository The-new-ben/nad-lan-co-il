# Dossier output contract (one JSON file per listing ID)

Write valid UTF-8 JSON to: /tmp/claude-0/-home-claude/65564abe-2682-55e6-800e-705f1cddbd65/scratchpad/meital/dossiers/<ID>.json
Validate it with: python3 -c "import json,sys; json.load(open(sys.argv[1]))" <file>

Rules
- Only verified facts. Every non-broker fact carries source_ids that exist in "sources". Never invent a number, a school, a distance, a developer or a date.
- confidence: "verified" (primary or two independent reputable sources), "likely" (one reputable source or strong inference, say why in note_en), "unverified" (weak or conflicting; explain).
- basis for numbers: "broker" (from the broker's Instagram), "source" (published figure), "computed" (your arithmetic on sourced figures; show the formula in note_en).
- Hebrew fields: natural, professional Israeli real estate Hebrew. English fields: natural international English. Numbers as digits. Currency NIS in English, ש״ח or ₪ in Hebrew.
- Do not use em dashes or en dashes anywhere (no U+2013, no U+2014). Use hyphens, commas or colons.
- Distances: only from a source, or computed straight-line from sourced coordinates (say "straight line"), or broker-stated (basis "broker"). Walking minutes only if a source gives them.
- Market comps: prefer 2025-2026 transactions (kind "transaction") over asking prices (kind "asking"). Give date, address or project, rooms, sqm, price, price per sqm (computed if not given), source.
- If you find the SAME unit listed elsewhere (another portal or broker) with price, floor or address, report it under "cross_listings" with the evidence that it is the same unit. Do not treat a similar unit as the same one.
- Access limits: if a site cannot be fetched, do NOT try other ways to fetch it. Note it in "access_notes".

JSON shape
{
  "id": "L04",
  "identification": {"summary_en": "...", "summary_he": "...", "address_or_project_en": "...", "address_or_project_he": "...", "confidence": "verified|likely|unverified", "evidence": ["..."], "source_ids": ["S1"]},
  "cross_listings": [{"what_en": "...", "url": "...", "date": "...", "price_nis": null, "details_en": "...", "same_unit_evidence_en": "...", "confidence": "likely"}],
  "building_facts": [{"label_en": "Developer", "label_he": "יזם", "value_en": "...", "value_he": "...", "basis": "source", "confidence": "verified", "source_ids": ["S2"], "note_en": ""}],
  "neighborhood_facts": [ same shape ],
  "distances": [{"to_en": "Tzuk beach", "to_he": "חוף הצוק", "value_en": "about 600 m, straight line", "value_he": "כ-600 מ׳ בקו אווירי", "basis": "computed|source|broker", "source_ids": [], "note_en": ""}],
  "schools": [{"name_en": "...", "name_he": "...", "level_en": "Elementary (1-6)", "level_he": "יסודי (א-ו)", "note_en": "nearby per Madlan; registration zone not verified", "note_he": "...", "source_ids": []}],
  "transport": [{"item_en": "...", "item_he": "...", "status_en": "operating|under construction, expected 2028", "status_he": "...", "source_ids": []}],
  "planning_future": [{"item_en": "...", "item_he": "...", "impact_en": "...", "impact_he": "...", "source_ids": []}],
  "market_stats": [{"metric_en": "...", "metric_he": "...", "value_en": "...", "value_he": "...", "as_of": "2026-08", "source_ids": []}],
  "sale_comps": [{"date": "2026-03-31", "where_en": "...", "where_he": "...", "rooms": "4.5", "sqm": 130, "floor": null, "price_nis": 5700000, "price_per_sqm_nis": 43846, "kind": "transaction|asking", "source_ids": [], "note_en": ""}],
  "rent_comps": [{"date": "...", "where_en": "...", "where_he": "...", "rooms": "5", "sqm": 128, "rent_nis": 16000, "rent_per_sqm_nis": 125, "kind": "asking|reported", "source_ids": [], "note_en": ""}],
  "costs": [{"item_en": "Building management fee", "item_he": "דמי ניהול", "value_en": "NIS 600 per month", "value_he": "600 ש״ח לחודש", "basis": "broker|source|computed", "source_ids": [], "note_en": ""}],
  "risks": [{"en": "...", "he": "...", "source_ids": []}],
  "buyer_or_renter_questions": [{"en": "...", "he": "..."}],
  "gaps": [{"en": "...", "he": "..."}],
  "access_notes": ["..."],
  "sources": [{"id": "S1", "title": "...", "url": "https://...", "published": "YYYY-MM-DD or accessed 2026-09-16"}]
}
