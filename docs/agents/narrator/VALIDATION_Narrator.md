# Narrator — Validation: Behavioral Invariants and Output Verification

```
STATUS: DRAFT
CREATED: 2024-12-19
UPDATED: 2025-12-19
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Narrator.md
BEHAVIORS:       ./BEHAVIORS_Narrator.md
ALGORITHM:       ./ALGORITHM_Scene_Generation.md
THIS:            VALIDATION_Narrator.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_Narrator.md
TEST:            ./TEST_Narrator.md
SYNC:            ./SYNC_Narrator.md

IMPL:            agents/narrator/CLAUDE.md
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run validation checks.

---

## BEHAVIORS GUARANTEED

| Behavior ID | Behavior | Why This Validation Matters |
|-------------|----------|-----------------------------|
| B1 | Major authored scenes release their canonical text and clickable layouts before any free-input fallback appears in the stream. | Guarantees deterministic storytelling so clients know when to stop generating their own continuations, giving health checks a fixed anchor to compare the stream shape against the graph state and preventing the player from seeing tentative drafts. |
| B2 | Every clickable reference is emitted with its key, display span, and waitingMessage/response pairing before player action is accepted. | Keeps the UI mapping stable while reducing phantom clickables, ensuring downstream tooling never has to guess whether a highlight matches the visible prose and giving the doctor a concrete contract to validate before the scene resolves. |
| B3 | Invented facts and mutations persist to the graph prior to the narrator closing the final chunk of the scene. | Makes the graph the single source of truth, so later narration can re-query the same facts without re-generating them and health monitors can verify the mutation batch before the stream presents those truths to the player. |

---

## OBJECTIVES COVERED

| Objective | Validations | Rationale |
|-----------|-------------|-----------|
| Preserve narrative continuity and authorial intent across sessions | V1, V3, V4 | Keeping conversational scenes lightweight while routing significant beats through SceneTree payloads protects canon, and voice consistency ensures each character remains recognizable so the narrator stays aligned with the graph-derived story plan. |
| Deliver responsive player interactions with valid clickables and timely streams | V2, V5 | Streaming the first chunk immediately and emitting clickable metadata before accepting input keeps the experience snappy and prevents dead UI targets, so every click feels intentional. |
| Maintain graph integrity while sharing mutations with downstream services | V3, V6 | Persisting invented facts plus schema validation of every mutation prevents downstream ingestion from encountering malformed data, letting health tooling assert that narrative updates never break the canonical store. |

---

## INVARIANTS

Narrator invariants must hold even when the graph is large, sessions persist for hours, and authorial prompts evolve; they are the contractual guardrails for every narrated scene.

### V1: Action Classification

- Conversational (<5 min): `scene: {}` only, with no `time_elapsed` field
  present, keeping output lightweight for short exchanges.
- Significant (>=5 min): full SceneTree payload plus `time_elapsed` to
  signal elapsed narrative time and justify state mutation.

### V2: Immediate Response

- First dialogue chunk must stream before any graph query to preserve a
  responsive feel even if retrieval work takes longer than expected.

### V3: Invention Persistence

- Every invented fact appears as a mutation so the graph remains the
  canonical memory store for authored narrative updates.
- Mutations must link to existing graph nodes (or nodes in the same batch)
  to avoid creating dangling references in the living graph.

### V4: Character Voice Consistency

- Dialogue matches each character's defined tone, diction, and cadence so
  voices remain recognizable across repeated interactions.

### V5: Clickable Validity

- Clickable keys appear in the text they annotate, ensuring the UI can map
  highlights to visible tokens without brittle fallbacks.
- Each clickable has either a response or a waitingMessage to prevent dead
  click targets that stall player interaction.

### V6: Mutation Schema Compliance

- Mutations validate against `engine/models/` schemas so downstream services
  can safely apply them without additional defensive coercion.

---

## PROPERTIES

- `SceneTree` and `NarratorOutput` payloads are shaped by the same schema the renderer consumes, so clients can trust the stream without runtime coercion.
- Clickable metadata pairs (key, span, waitingMessage/response) mirror the UI contract, keeping every highlight mapped to a visible segment before input is accepted.
- Mutation batches are only persisted after being validated against the graph schemas, ensuring every invented fact joins the canonical memory with the right references.

---

## ERROR CONDITIONS

- `MissingScenePayload`: emitted when a significant scene fails to include the SceneTree payload that downstream services require.
- `ClickableMismatch`: raised if a clickable key or span is missing while the narration still references the highlighted text, preventing unusable UI targets.
- `MutationSchemaViolation`: triggered by the schema validator in `Health` when a mutation batch contains unexpected fields, guarding the graph from malformed updates.

---

## HEALTH COVERAGE

- `author_coherence` health indicator relies on `HEALTH_Narrator.md` checkers and traces back to invariants V1, V3, and V4 to keep story facts aligned with the graph.
- `mutation_validity` depends on the `mutation_safety_checker`, which enforces V3 and V6 by running the schema validator before committing invented facts.
- The Narrator health flows include manual `pytest engine/tests/test_narrator_integration.py` runs so the invariants stay validated whenever the health suite replays recent scenes.

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] V1 holds (classification + time_elapsed)
[ ] V2 holds (first chunk < 2s)
[ ] V3 holds (inventions persisted)
[ ] V4 holds (voice consistency)
[ ] V5 holds (clickables valid)
[ ] V6 holds (schemas validate)
```

### Automated (if available)

```bash
pytest engine/tests/test_narrator_integration.py
python tools/validate_narrator_output.py --check clickables
```

---

## TEST COVERAGE (Snapshot)

| Requirement | Status |
|-------------|--------|
| V1 Classification | Spot-checked in recent manual runs; no automated guard. |
| V2 Immediate response | Not automated; timing is observed ad hoc in dev. |
| V3 Invention persistence | Partial coverage via mutation schema checks only. |
| V4 Voice consistency | Manual review during authoring sessions and QA. |
| V5 Clickable validity | Spot-checked when reviewing generated scene text. |
| V6 Mutation schema | Covered by schema validation and model tests. |

---

## PROPERTIES

- Persisted mutations tie every authored beat to the graph before emitting the final chunk so downstream queries always see the same state.
- Scene streaming always begins within a few seconds and ships each chunk with metadata so the CLI remains responsive while graph reads finish.
- Clickable metadata includes keys, spans, and response references to keep UI mapping deterministic without fallback heuristics.

---

## ERROR CONDITIONS

- `GraphMutationFailure`: When the engine rejects the mutation batch due to schema or constraint violations, the narrator must abort and report before streaming the mutated facts.
- `MissingClickableMapping`: Triggered when a clickable key is missing from the emitted text, indicating a tooling bug that prevents the UI from resolving the click target.
- `StreamTimeout`: Fires when the first chunk does not start within the expected latency window, implying a blocking graph read or prompt issue that needs investigation.

---

## HEALTH COVERAGE

- `schema_validator` compares SceneTree outputs against `HEALTH_Narrator` expectations so V1–V6 remain schema-compliant and traceable to the health doc.
- `mutation_safety_checker` asserts every invented fact obeys graph constraints before the narrator returns control, directly anchoring V3.
- `pytest engine/tests/test_narrator_integration.py` is the manual entrypoint referenced in the health doc to confirm V2 latency, clickable sequencing, and streaming flows.

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-19
VERIFIED_BY: ngram repair agent
RESULT: Added missing SYNC status and expanded validation detail; runtime verification not run in this repair.
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Automated voice consistency scoring to reduce subjective review burden.
- [ ] Property-based tests for mutation integrity across edge-case payloads.
- [ ] Regression tests for classification drift on conversational thresholds.
- QUESTION: How to validate seeds -> payoff tracking without subjective tags?
