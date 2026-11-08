# Justice reuse forward test

Tested 8 November 2026. Request: “Reuse our talking character work to prepare an English-speaking guide for Justice, using what is already on Ben’s PC and no paid service. Tell me what can be reused and what needs to be established; do not publish anything.”

Decision: prepare a separate, local Justice product-guide configuration using the existing browser and offline speech components. Do not copy the NadLan persona, portrait approval, buying-guide knowledge or live deployment configuration. No new character generation is needed for this preparation.

## Concrete reuse and handoff

| Reuse | Implementation decision |
|---|---|
| Browser lifecycle, audio and lip timing | Start from `prototype-3d/widget-stream.js`, `stream-player.js` and `dynamic-lips.js`. Preserve trusted first interaction, explicit microphone permission, persistent close, request-token cancellation, stale-result rejection and the playing audio clock. Adapt the host integration after choosing the Justice surface; the court repository currently specifies docked panels, so a floating NadLan widget is not an automatic fit. |
| Existing local English inference | Reuse the existing voice environment and offline `speech_worker.py` path with Whisper small and Chatterbox Multilingual V2. The source explicitly disables network connections and loads cached weights. Qwen3-1.7B Q8 and its executable are present. This proves files and implementation, not that a new conversation will run within available memory. Do not silently select Turbo ONNX or rebuild the environment. |
| Geometry and existing portraits | Reuse the Blender preparation/export method if a small 3D guide is chosen. The existing NadLan GLB is a narrow frontal surface, not a full head. The court avatar bank already contains professional portraits and generated seeds, including mediator, attorney and party roles. Review these existing assets before creating anything; their presence does not approve a specific Justice guide or voice pairing. |
| Speech preparation and prior comparisons | Reuse the voice index and checked-path manifest, including existing English Kokoro comparison audio and VibeVoice text preparation. Kokoro is an optional comparison with historical outputs, not a replacement approved by this request. Do not call the Hebrew gateway, which may wake a paid GPU. |
| Transport patterns | Reuse session ownership, CSRF, bounded uploads, job cancellation and private audio delivery patterns. The live NadLan WordPress relay is not Justice infrastructure. No relay, listener, tunnel or deployment is created by this handoff. |

Before implementation, establish these specific inputs:

1. **Target:** Justice’s WordPress information site at `jus-tice.co.il`, or the product at `jus-tice.com`, with the exact page/module and guide placement. The court North Star distinguishes these surfaces. This request does not choose one.
2. **Guide role and knowledge:** limit the proposed first guide to explaining the selected product journey. Recover approved current English product content, source dates and unknown-answer behavior. A simulated judge, lawyer and product guide are different roles. The existing `brain.py` has NadLan-specific retrieval synonyms, `SOURCE_URL`, saved property content and persona rules; changing the display name is insufficient. Do not claim legal qualifications, case outcomes or completed professional actions.
3. **Identity and presentation:** choose an existing fictional adult portrait and an approved English voice/reference for this project. The NadLan reference remains available as a comparison, not automatically selected. Retrieve current Justice palette and typography from the chosen surface before a Claude Design brief. The old court design specification still contains gold accents, while the later cockpit brief rejects the cream/brown direction; neither authorizes importing NadLan colors.
4. **Acceptance and operation:** review pronunciation, voice identity and subtle mouth behavior with fixed English product examples; test real microphone and typed flows, cancellation, failure and surrounding controls. Check current memory without loading models, keep the existing reserve, then measure a genuinely fresh end-to-end turn if authorized. Set a project-specific tracking context without inheriting HAD-682 deployment permission. No tracking messages or external writes were made in this test.

## Readiness boundary

The latest shared index records a published NadLan greeting and controls, but a real public question returned 503 because of insufficient memory. The backend document records a historical fresh microphone pipeline of 236.093 seconds. Neither is a Justice readiness or conversational-latency claim. This forward test ran no models, performed no listening or browser test, spent nothing, contacted nobody and published nothing. The only new file is this handoff.

## Skill findings

- The first read caught two links removed during compaction. A fresh read of the completed skill resolved them to section anchors in `operations.md` and `domain-adaptation.md`; all local Markdown file targets in those three files now exist. This is resolved, not an outstanding defect.
- One concrete navigation gap remains: the Justice section says to read the “shared talking-agent index” without linking or naming its path. That index is needed to find the court bank and prior bake-off. This test found it through the machine instructions, not the skill itself. Add the explicit `../../../TALKING-AGENT.md` link there so a fresh agent following only the package does not need that unstated context.
- The instructions prevented two plausible wrong implementations: treating the published NadLan relay as a currently working public conversation, and dressing its approved woman as a Justice judge. The source inspection also caught the hard-coded real-estate brain and court docked-panel constraint before any code change.

## Sources actually followed

Canonical skill and its operations/domain-adaptation references; `C:/Users/777/Documents/agent-tools/TALKING-AGENT.md`; `VOICE-REUSE-INDEX.md` and `voice-reuse-index.json`; `prototype-3d/BACKEND.md`, `brain.py` and `speech_worker.py`; `C:/Users/777/Documents/ChatGPT-Work/courtai/AGENTS.md`, `docs/AVATAR_BANK_SPEC.md`, `docs/HADMAIA-PHOTOREAL-AVATAR-FACTORY-2026-09-06.md`, `docs/JUSTICE-NORTH-STAR-GOAL-HE-2026-08-27.md`, `docs/JUSTICE-JURIS-COCKPIT-HOMEPAGE-2026-08-27.md`, the opening design-token section of `docs/DESIGN_SYSTEM_SPECIFICATION.md`, and the avatar imports/resolver in `src/juris-arena/ui/components/ArenaAvatarCard.tsx`. No earlier forward-test conclusions were read.
