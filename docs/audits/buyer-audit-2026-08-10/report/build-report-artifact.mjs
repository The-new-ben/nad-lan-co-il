/**
 * Builds the canonical, portable report artifact from the reviewed package data.
 * The generated artifact contains no machine-local paths, credentials or tokens.
 */
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(here);
const generatedAt = "2026-08-10T23:30:00+03:00";

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    if (quoted) {
      if (char === '"' && text[index + 1] === '"') { field += '"'; index += 1; }
      else if (char === '"') quoted = false;
      else field += char;
    } else if (char === '"') quoted = true;
    else if (char === ",") { row.push(field); field = ""; }
    else if (char === "\n") { row.push(field.replace(/\r$/, "")); rows.push(row); row = []; field = ""; }
    else field += char;
  }
  if (field || row.length) { row.push(field); rows.push(row); }
  const header = rows.shift();
  return rows.filter((values) => values.length && values.some(Boolean)).map((values) =>
    Object.fromEntries(header.map((key, index) => [key, values[index] ?? ""]))
  );
}

const gaps = parseCsv(await fs.readFile(path.join(root, "data", "buyer-question-gap-matrix.csv"), "utf8"));
const stateCounts = Object.entries(gaps.reduce((counts, row) => {
  counts[row.current_state] = (counts[row.current_state] || 0) + 1;
  return counts;
}, {})).map(([state, count]) => ({
  state,
  count,
  share_percent: Math.round((count / gaps.length) * 1000) / 10,
  total_questions: gaps.length,
  interpretation: state === "MISSING" ? "No one-click decision answer" :
    state === "INVENTED" ? "The current journey presents an unsupported substitute" :
    state === "CONTRADICTED" ? "Credible sources disagree" :
    state === "SOURCED_ESTIMATE" ? "Useful only with source and assumptions" : "Observed/verified answer"
})).sort((a, b) => b.count - a.count);

const focusIds = ["G013", "G031", "G024", "G008", "G020", "G041", "G053", "G069", "G079", "G103", "G142", "G145"];
const focusRows = focusIds.map((id, index) => {
  const row = gaps.find((candidate) => candidate.gap_id === id);
  if (!row) throw new Error(`Missing focus gap ${id}`);
  return {
    priority_rank: index + 1,
    gap_id: row.gap_id,
    journey_stage: row.journey_stage,
    buyer_question: row.buyer_question,
    current_state: row.current_state,
    severity: row.severity,
    decision_risk: row.decision_risk,
    data_owner: row.data_owner,
    one_click_surface: row.one_click_surface,
    required_evidence: row.evidence_required,
    acceptance_test: row.acceptance_test
  };
});

const p0Count = gaps.filter((row) => row.severity === "P0").length;
const inventedCount = gaps.filter((row) => row.current_state === "INVENTED").length;

const sources = [
  { id: "live-audit", label: "Live ToHa2 and THE PARK browser/source audit", path: "research/live-audit-findings.md" },
  { id: "toha-dossier", label: "ToHa2 buyer due-diligence dossier", path: "research/toha2-buyer-dossier.md" },
  { id: "park-dossier", label: "THE PARK buyer due-diligence dossier", path: "research/the-park-buyer-dossier.md" },
  { id: "competitor", label: "Competitor UX benchmark", path: "research/competitor-benchmark.md" },
  {
    id: "gap-matrix",
    label: "150-question buyer gap matrix",
    path: "data/buyer-question-gap-matrix.csv",
    query: {
      engine: "DuckDB",
      sql: "SELECT * FROM read_csv_auto('data/buyer-question-gap-matrix.csv', header=true);",
      description: "Read the complete atomic buyer-question matrix without filtering.",
      executed_at: generatedAt,
      language: "SQL",
      tables_used: ["data/buyer-question-gap-matrix.csv"],
      filters: ["No rows excluded"]
    }
  },
  {
    id: "gap-metrics",
    label: "Buyer gap headline metrics",
    path: "data/buyer-question-gap-matrix.csv",
    query: {
      engine: "DuckDB",
      sql: "SELECT COUNT(*) AS questions, SUM(CASE WHEN severity='P0' THEN 1 ELSE 0 END) AS p0, SUM(CASE WHEN current_state='INVENTED' THEN 1 ELSE 0 END) AS invented FROM read_csv_auto('data/buyer-question-gap-matrix.csv', header=true);",
      description: "Count all audited questions, P0 rows and invented-answer rows.",
      executed_at: generatedAt,
      language: "SQL",
      tables_used: ["data/buyer-question-gap-matrix.csv"],
      filters: ["No rows excluded"],
      metric_definitions: [
        "questions = count of all atomic question rows",
        "p0 = rows whose severity equals P0",
        "invented = rows whose current_state equals INVENTED"
      ]
    }
  },
  {
    id: "gap-states",
    label: "Buyer questions aggregated by evidence state",
    path: "data/buyer-question-gap-matrix.csv",
    query: {
      engine: "DuckDB",
      sql: "WITH counts AS (SELECT current_state AS state, COUNT(*) AS count FROM read_csv_auto('data/buyer-question-gap-matrix.csv', header=true) GROUP BY 1) SELECT state, count, ROUND(100.0 * count / SUM(count) OVER (), 1) AS share_percent FROM counts ORDER BY count DESC;",
      description: "Aggregate all audited questions by their reviewed current evidence state.",
      executed_at: generatedAt,
      language: "SQL",
      tables_used: ["data/buyer-question-gap-matrix.csv"],
      filters: ["No rows excluded"],
      metric_definitions: ["count = questions in each current_state", "share_percent = state count divided by all questions"]
    }
  },
  {
    id: "gap-priority",
    label: "Twelve first release gates selected from the buyer matrix",
    path: "data/buyer-question-gap-matrix.csv",
    query: {
      engine: "DuckDB",
      sql: "SELECT * FROM read_csv_auto('data/buyer-question-gap-matrix.csv', header=true) WHERE gap_id IN ('G013','G031','G024','G008','G020','G041','G053','G069','G079','G103','G142','G145');",
      description: "Select the twelve cross-functional first release gates shown in the executive table; the complete matrix remains available separately.",
      executed_at: generatedAt,
      language: "SQL",
      tables_used: ["data/buyer-question-gap-matrix.csv"],
      filters: ["gap_id restricted to the twelve explicitly listed release gates"]
    }
  },
  { id: "data-dictionary", label: "Commercial/residential evidence data dictionary", path: "data/data-dictionary.csv" },
  { id: "lead-audit", label: "Lead ownership and routing audit", path: "research/lead-routing-audit.md" },
  { id: "ux-spec", label: "Commercial decision-surface UX specification", path: "ux/ux-spec.md" },
  { id: "migration", label: "Sandbox-first migration and QA plan", path: "migration-and-qa.md" },
  { id: "source-register", label: "Research source register", path: "research/source-register.md" }
];

const title = "Nadlan 360° Moment-of-Truth Audit — ToHa2, THE PARK and the 3D Decision Engine";
const blocks = [
  {
    id: "title",
    type: "markdown",
    layout: "full",
    body: `# ${title}\n\n**Evidence cut-off:** 10 August 2026 · **Audience:** product, commercial, data, design and engineering teams · **Status:** read-only audit and proposal; no live change.\n\nThis report asks one hard question: can an American company that has never operated in Israel select an exact floor, understand the place, price and infrastructure, trust the evidence, and reach an accountable human without leaving the page or guessing?`
  },
  {
    id: "executive-summary",
    type: "markdown",
    layout: "full",
    body: `## Executive conclusion\n\n**No. Neither commercial page is currently decision-ready, despite unusually rich editorial research and a genuinely differentiating 3D theatre.** The model should stay. The transaction layer around it must change.\n\nThe decisive failure is not merely missing copy. A floor click can resolve to a different floor because 44 or 75 fixed-size hotspots overlap. Missing status is converted to available; whole floors are presented as west-facing; office floors inherit apartments, rooms, balconies and synthetic bedrooms; all-in rent and infrastructure are absent; the context map is a single project pin; and enquiries fall to an administrator because neither project has an accountable owner route.\n\nThe package maps ${gaps.length} atomic buyer questions. ${p0Count} are P0 decision/release gaps and ${inventedCount} are not merely missing: the current experience supplies an unsupported substitute. The recommended product is one evidence-backed decision surface synchronized to the exact building, floor and suite. Unknowns stay visible and can be requested in one click.`
  },
  { id: "metric-strip", type: "metric-strip", layout: "full", cardIds: ["questions", "p0", "invented"] },
  {
    id: "coverage-intro",
    type: "markdown",
    layout: "full",
    body: `## Buyer-answer coverage\n\nThe gap inventory is intentionally demanding. It covers legal identity, availability, floor geometry, cost, fit-out, MEP, telecoms, vertical transport, access, commute, traffic, daily life, market evidence, language, privacy and lead response. Missing and invented states dominate. A polished placeholder does not count as an answer.`
  },
  { id: "coverage-chart", type: "chart", layout: "full", chartId: "gap-state-chart" },
  {
    id: "moment-of-truth",
    type: "markdown",
    layout: "full",
    body: `## The current moment of truth\n\n1. **Selection is unreliable.** Attempts to choose floor 20 resolved to ToHa floors 24/23 and THE PARK floors 22/21 across mobile/desktop samples. The interface cannot truthfully attach downstream facts or a lead to “the selected floor.”\n2. **Availability is fail-open.** The live data marks all 75 ToHa floors and all 44 Park floors available, while no live owner schedule is connected. The production sanitizer defaults missing/invalid status to available.\n3. **The product uses the wrong noun.** Offices are rendered as homes with zero rooms, balconies, apartment tours and an apartment designer.\n4. **Evidence tools are shells.** Plan is empty, View is illustrative, Tour manufactures bedrooms, Studio designs a home, and Compare uses residential fields.\n5. **Location is not a decision map.** One project marker and straight-line distances do not answer peak commute, entrance, operating versus planned transit, daily life, business ecosystem, market or risk.\n6. **Useful research is disconnected.** ToHa availability/price content sits roughly 21,000–23,000 px down; THE PARK power/fiber/cost content sits roughly 15,000–26,000 px down.\n7. **The lead has no accountable project route.** Both cards are unclaimed with no owner; current routing therefore falls to the generic administrator path.`
  },
  {
    id: "priority-table-intro",
    type: "markdown",
    layout: "full",
    body: `## Twelve release-critical questions\n\nThese are the first gates, not the whole backlog. The full 150-row matrix names the owner, exact evidence, one-click placement and acceptance test for every question.\n\n${focusRows.map((row) => `${row.priority_rank}. **${row.buyer_question}** — ${row.current_state}, ${row.severity}.`).join("\n")}`
  },
  {
    id: "project-research-toha",
    type: "markdown",
    layout: "full",
    sourceId: "toha-dossier",
    body: `## ToHa2: credible project, unknown lease product\n\nPublic evidence supports a major ToHa2 project, a highly connected HaShalom/Yigal Alon location, material Google commitment and active construction. It does **not** prove which floors are available, what area a tenant pays for, the asking terms, technical capacity, floor-specific handover or final certification.\n\nThe public record conflicts on 75/77/80 floors; several area scopes from 100,000 to 201,000 m² are mixed; Q4 2026 completion, end-2026 Form 4 and Q1 2027 occupancy are collapsed into one story; and 60 versus 70 lifts appear in public material. These values can describe different scopes, but the page must not silently choose one.\n\nThe exact owner artifacts required are a current floor crosswalk/stacking plan, signed availability feed, certified area schedule and measurement standard, commercial term sheet, tenant technical handbook, MEP/structural schedules, carrier letters, elevator schedule/performance, access/loading/fire/accessibility packs and final certificate IDs.`
  },
  {
    id: "project-research-park",
    type: "markdown",
    layout: "full",
    sourceId: "park-dossier",
    body: `## THE PARK: shortlist candidate, not yet approvable\n\nOwner and statutory material support a substantial office/retail project beside Bnei Brak rail, broad floorplates, terraces and an under-construction/completion story. They do not supply the floor inventory, legal/elevator/marketing numbering crosswalk, certified net/gross areas, owner commercial terms, Form 4 scope or technical/fit-out pack needed to approve a headquarters.\n\nThe public record conflicts on 44 versus 52 floors; a statutory disclosure refers to 45 office floors above three retail levels. Zone numbering shifts by seven floors between plan generations. Completion/move-in claims span historic Q4 2024/Q1 2025, Q3 2026 and 2027. Full Green Line operation is an official future benefit, not current service.\n\nThe product must keep the project in comparison as “owner documentation required,” not present 44 green available floors.`
  },
  {
    id: "competitor-synthesis",
    type: "markdown",
    layout: "full",
    sourceId: "competitor",
    body: `## What the best competitors teach\n\nNo single competitor is complete. The target combines:\n\n- **LoopNet/CoStar:** space-level floor/suite rows, condition, delivery, rents, comps, tenants and stacking-plan depth;\n- **Compass:** a coherent dossier and media dialog that retains identity, Save, Share, Contact and predictable Back;\n- **Zillow:** personalized, mode-based commute feasibility and saveable map state;\n- **Rightmove:** route-backed media, explicit unknown/“ask agent” fields and mobile contact continuity;\n- **nadlan.gov.il and Israeli platforms:** local transaction, planning and neighborhood evidence;\n- **Booking/Airbnb patterns:** legible nearby/facility categories, evidence labels, media and accessibility context.\n\nThe competitive opening is not more prose. It is a single synchronized surface where model, selected floor, live availability, plan, all-in cost, infrastructure, commute, records, unknowns, comparison and the exact adviser question stay together.`
  },
  {
    id: "recommended-ux",
    type: "markdown",
    layout: "full",
    sourceId: "ux-spec",
    body: `## Recommended one-click decision surface\n\n**Primary architecture — in-place canonical state:** keep the project page and live 3D engine mounted. One atomic render replaces the prompt/inventory state with the selected asset; URL, model highlight, identity, exposure, facts, tools and enquiry context stay synchronized. The project/asset URL is accepted only on the exact site origin and canonical WordPress permalink, and history commits before any visible model, picker or decision-state mutation. A failed history/dialog/controller/cleanup step restores the prior URL, model, picker, focus, scroll, inert and document-lock state rather than leaving a partial or uncloseable surface.\n\n**Mobile:** one viewport contains a live model strip, exact identity/status, an always-visible local map with calibrated facade beam(s) and truthful in-sector landmarks, three evidence-aware facts, four 2×2 doors, Save/Compare/Share and one commercial CTA. A whole office floor shows every verified exposure rather than an invented single “window direction.” Every fixed-scene landmark uses separately evidenced full and localized compact labels (1–12 Unicode code points); nobody derives or truncates them, and any rejected compact-label claim neutralizes the whole scene. Unknown geometry renders a neutral request state, not a cone or promised view. No prior hero residue, fixed bar overlap or inner scroll. **Desktop:** the model stays live; a 430 px decision rail sits beside it. Heavy evidence opens in a body-level full-screen dialog and returns in one action to the same camera, floor, focus and scroll.\n\n**Viable alternative — dedicated selected-asset route:** if the accumulated page/theme lifecycle cannot pass two sandbox/physical-phone iterations, navigate to a canonical server-rendered floor/suite route. It must render the same live model strip, one-view beam/facts/doors/CTA and body-level tools—never a bottom sheet or nested frame—and Browser Back must restore the picker/camera/scroll. It offers stronger CSS/cache/error isolation and shareable floor URLs, at the cost of navigation latency, WordPress rewrite/template complexity and explicit model-state restoration.\n\nThe four doors are: **Floor pack**, **Fit-out & infrastructure**, **Commute & area**, and **Cost & records**. Each either opens verified evidence or honestly offers “Request the verified item.” Both architectures use the same route-backed data/lead contract. The interactive offline wireframe demonstrates the preferred in-place version.`
  },
  {
    id: "truth-contract",
    type: "markdown",
    layout: "full",
    sourceId: "data-dictionary",
    body: `## The engine contract: asset type plus evidence envelopes\n\nUse one runtime enum: \`residential | commercial_office | retail | mixed_use | hospitality | guide_only\`. Product-family labels such as premium and 3D are separate capabilities. Never infer an office from \`rooms = 0\`. A type with no approved adapter remains non-selectable. Commercial UI status is exactly \`unknown | verified_available | soft_hold | under_offer | under_loi | leased | delivered | unavailable | not_marketed\`. The eight non-unknown values are the stored business enum; an unknown evidence envelope stores \`value: null\` and derives the ninth presentation status. **Unknown is the only default.**\n\nEvery material field carries value, unit, state (\`unknown | source_estimate | verified | contradictory\`), scope, effective date, sources and observations, verification/expiry dates, accountable owner, confidence, reason/applicability, conflict IDs, note/caveat, required documents and decision grade. The browser changes field casing only and never invents provenance. Selection identity is the immutable browser/content \`project_contract_id + building_id + tower_id + floor_id (+ suite_id)\` tuple; even one-tower projects publish an explicit building/tower registry, so equal floor labels in two towers cannot collide. A separate numeric WordPress routing key is carried as \`wp_post_id\` in project data and \`project_id\` on the RFP wire, but it never replaces the contract tuple. A whole office floor has an exposures array and one independently evidenced beam per facade, not one “window direction.” Area separates rentable/gross, usable/net and measurement standard. Price separates base rent, management, arnona, parking, utilities, VAT, incentives and fit-out amortization.\n\nThe package includes a 240-field dictionary, a complete 149-row gap-to-field crosswalk and honest non-publishable example payloads. The same truth primitive powers residential and premium product families; each runtime asset type renders only through its approved adapter.`
  },
  {
    id: "implementation",
    type: "markdown",
    layout: "full",
    body: `## Concrete implementation proposal\n\nThe \`proposed-code/\` directory contains complete, proposal-only vanilla JS, CSS and classic WordPress PHP:\n\n- model-space floor hit testing with explicit non-overlapping tower-scoped ranges and a native picker;\n- one scene-host lifecycle that keeps the existing live model and decision surface simultaneously visible at mobile, short-landscape and desktop sizes;\n- evidence-aware selected-floor rendering with a fixed, truth-gated local map and one independently evidenced facade beam per exposure plus in-sector landmarks;\n- body-level full-screen tool lifecycle, focus trap, transactional history and scroll restoration that cannot strand inert/locked UI when history, dialog or cleanup fails;\n- an existing-Mapbox context explorer with operating/planned/closed states, sourced points/routes, bounded pagination, actionable sources/requests and a readable failure fallback;\n- a strict commercial data normalizer with unknown-by-default truth;\n- a complete five-locale HE/EN/FR/RU/AR dictionary with RTL/logical affordances and curiosity-led commercial copy;\n- a bounded five-step vanilla-JS RFP composer plus consent-aware, durable-idempotent WordPress case route with immutable project/building/tower/floor/suite context, accountable routing, opaque case ID and SLA confirmation;\n- an isolated signed test-sink route that cannot send sandbox requests to production mail, CRM, routing or analytics;\n- a guarded classic-WordPress sandbox integration that loads after the existing showroom handle and injects the isolated CSS through \`wp_add_inline_style\`;\n- responsive CSS with no \`overflow:auto|scroll\`, no \`inset\` shorthand and explicit safe-area handling.\n\nExecutable PHP, Node and real-Chromium fixtures cover the server-to-browser adapter, multi-beam/map truth, tower-scoped identity, exact-origin/canonical-permalink route validation, transactional model/picker/history rollback, injected History/dialog/cleanup failure, model-host geometry, five-locale completeness, context-map fallback/action reachability, RFP payload/retry/recovery, isolated sandbox sink, durable crash-resume idempotency and WordPress load order. Known historical traps are explicitly avoided: transformed ancestors containing fixed layers, observers mutating what they watch, cascade-prone inset shorthand, duplicate responsive subtrees, stale history markers and hidden transition states that steal focus.`
  },
  {
    id: "lead-routing",
    type: "markdown",
    layout: "full",
    sourceId: "lead-audit",
    body: `## Contact must produce an accountable answer\n\nOne lead composer accepts many contextual entry points. Every missing field can add its question and required document to one RFP basket. The submission automatically retains project, floor, suite, data version, locale and selected questions. It asks company, role, headcount, growth, move date, area, budget and special uses.\n\nA successful response names an opaque case ID, receiving team category and human response target. Routing is explicit per commercial project and independent of advertising tier. A safe Nadlan commercial desk is the fallback. The buyer never sees an internal email/user ID, and sensitive free text never goes to general analytics.\n\nReal delivery must be tested only against seeded test recipients before release. No real lead was submitted during this audit.`
  },
  {
    id: "migration",
    type: "markdown",
    layout: "full",
    sourceId: "migration",
    body: `## Migration and release order\n\nBuild in a password-protected, noindex sandbox behind per-project feature flags. Both the password challenge and authenticated response must be private/no-store; if the literal cache opt-out or exact headers cannot be confirmed, protected assets, configuration and nonce stay blocked. A sandbox lead success is accepted only as a visible synthetic \`TEST-*\` case with \`test_sink\` route/delivery/status and zero SLA; production and test acknowledgements are mutually rejected. Each phase has a phone gate and rollback: truth contract → exact selection → asset-type adapter → one-screen surface → evidence tools → context map → cost/compare → RFP/routing → five languages/schema → performance/accessibility → controlled rollout.\n\nAcceptance covers 320×568 through 1440×900, portrait/landscape, physical owner phone, iPhone Safari, Android Chrome, touch, mouse, keyboard, screen reader, 200% zoom, slow/offline behavior, Back/Forward, foreign/noncanonical navigation URLs, forced History API/dialog/cleanup failure with exact rollback, rotation while tools are open, data expiry, source conflicts, authenticated-then-anonymous cache reuse and test-only lead delivery.\n\nDo not expose a project publicly until exact selection, truthful availability, asset language, lead route and evidence-state gates pass.`
  },
  {
    id: "caveats",
    type: "markdown",
    layout: "full",
    body: `## Caveats and responsible use\n\nBrowser evidence is Chromium viewport testing, not a physical iPhone/Safari certification. Public sources cannot establish live landlord availability, signed terms, certified floor measurements or technical capacity. Those remain unknown until the named owner document/API is ingested. Competitor access limits and anti-bot/paywall cases are labeled in the benchmark. No outbound form, contact, appointment, callback, alert or login action was performed.\n\nThis is a product and engineering audit, not legal, tax, valuation, engineering, accessibility or leasing advice. A tenant should rely on executed lease exhibits, stamped drawings, current certificates and qualified advisers.`
  },
  {
    id: "package-map",
    type: "markdown",
    layout: "full",
    body: `## How to use the package\n\nStart with \`README-FIRST.md\`. Product/design should open this report and the interactive wireframe. Data/operations should work through the project fact matrices, 150-question gap matrix, 149-row field crosswalk and 240-field dictionary. Engineering should read \`proposed-code/README.md\` and \`migration-and-qa.md\`. Evidence reviewers can reproduce the live observations from the portable Playwright helpers and sanitized JSON under \`evidence/\`; fresh live runs remain new dated evidence. Every source URL is indexed in \`data/source-url-register.csv\`.`
  }
];

const artifact = {
  surface: "report",
  manifest: {
    version: 1,
    surface: "report",
    title,
    description: "Evidence-backed 360-degree buyer, UX, data, commercial and lead-routing audit for Nadlan's ToHa2 and THE PARK journeys, generalized to the 3D engine.",
    generatedAt,
    sources,
    cards: [
      { id: "questions", description: "Atomic questions a demanding foreign office occupier must be able to answer.", dataset: "audit_metrics", sourceId: "gap-metrics", metrics: [{ label: "Buyer questions audited", field: "questions", format: "number" }] },
      { id: "p0", description: "Questions whose failure can invalidate selection, truth, compliance, pricing or lead handoff.", dataset: "audit_metrics", sourceId: "gap-metrics", metrics: [{ label: "P0 decision/release gaps", field: "p0", format: "number" }] },
      { id: "invented", description: "Questions where the current experience presents an unsupported substitute rather than a neutral unknown.", dataset: "audit_metrics", sourceId: "gap-metrics", metrics: [{ label: "Invented-answer states", field: "invented", format: "number" }] }
    ],
    charts: [
      {
        id: "gap-state-chart",
        title: "Buyer questions by current evidence state",
        subtitle: "150 atomic questions; missing and invented answers are the principal product risk.",
        intent: "comparison",
        question: "How much of the buyer journey is actually answered?",
        rationale: "A horizontal bar makes the dominant missing state and smaller evidence states immediately comparable.",
        type: "horizontalBar",
        dataset: "gap_state_counts",
        sourceId: "gap-states",
        encodings: {
          x: { field: "state", type: "nominal", aggregate: "none", label: "Current evidence state" },
          y: { field: "count", type: "quantitative", aggregate: "none", format: "number", label: "Questions" },
          tooltip: [
            { field: "count", type: "quantitative", aggregate: "none", format: "number", label: "Questions" }
          ]
        },
        layout: "full",
        maxRows: 10,
        emptyState: "No audited questions were available."
      }
    ],
    tables: [],
    blocks
  },
  snapshot: {
    version: 1,
    generatedAt,
    status: "ready",
    datasets: {
      audit_metrics: [{ questions: gaps.length, p0: p0Count, invented: inventedCount, projects: 2, locales: 5 }],
      gap_state_counts: stateCounts,
      priority_gaps: focusRows
    }
  },
  sources
};

const serialized = JSON.stringify(artifact, null, 2) + "\n";
if (/C:\\Users\\|C:\/Users\/|pk\.[A-Za-z0-9]|access_token\s*[=:]|authorization\s*[=:]/i.test(serialized)) {
  throw new Error("Portable artifact contains a forbidden local or credential-like value");
}
await fs.writeFile(path.join(here, "artifact.json"), serialized, "utf8");
console.log(JSON.stringify({ blocks: blocks.length, questions: gaps.length, p0: p0Count, states: stateCounts, bytes: Buffer.byteLength(serialized) }));
