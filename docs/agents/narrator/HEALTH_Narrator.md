# Narrator — Health: Verification Mechanics and Coverage

```
STATUS: STABLE
CREATED: 2024-12-19
UPDATED: 2025-12-20
```

---

## PURPOSE OF THIS FILE

This file defines the health checks and verification mechanics for the Narrator module. It ensures the authorial intelligence produces coherent, schema-compliant story beats that correctly mutate the world state.

What it protects:
- **Authorial Coherence**: Logical consistency of narrated scenes with prior canon.
- **State Integrity**: Accuracy of graph mutations proposed by the agent.
- **UX Reliability**: Validity of clickables and interaction trees.

---

## WHY THIS PATTERN

HEALTH documentation sits beside tests so we can verify living flows without rewriting the runtime prompt stack. The narrator inhabits a high-variance space where streaming prose and mutable graphs intersect, so the health doc exists to name the docking points, failure cases, and intended observables while leaving the code untouched.

- **Failure mode avoided:** Losing track of the SceneTree schema or clickables before they hit the renderer, which would make story updates feel random even if the CLI is technically running.
- **Verification surface:** Docking to JSON output, mutation batches, and mutation schema checks gives the doctor a surface that is both human-readable and machine-verifiable.
- **Cadence managed:** These checks run separately from the narrator CLI so the health tracker can sample at a lower frequency without throttling production prompts.

## CHAIN

```
PATTERNS:        ./PATTERNS_Narrator.md
BEHAVIORS:       ./BEHAVIORS_Narrator.md
ALGORITHM:       ./ALGORITHM_Scene_Generation.md
VALIDATION:      ./VALIDATION_Narrator.md
IMPLEMENTATION:  ./IMPLEMENTATION_Narrator.md
THIS:            HEALTH_Narrator.md
SYNC:            ./SYNC_Narrator.md
```

> **Contract:** HEALTH checks verify intent and output without rewriting agent logic.

---

## FLOWS ANALYSIS (TRIGGERS + FREQUENCY)

```yaml
flows_analysis:
  - flow_id: scene_generation
    purpose: Transform player intent into authored story beats.
    triggers:
      - type: manual
        source: User interaction
    frequency:
      expected_rate: 1/min (active play)
      peak_rate: 5/min
      burst_behavior: Limited by LLM latency.
    risks:
      - Prompt injection or drift
      - Hallucinated mutations that break schema
```

---

## HEALTH INDICATORS SELECTED

```yaml
health_indicators:
  - name: author_coherence
    flow_id: scene_generation
    priority: high
    rationale: Narrator must respect the graph's "truth".
  - name: mutation_validity
    flow_id: scene_generation
    priority: high
    rationale: Invalid mutations can corrupt the playthrough state.
```

---

## OBJECTIVES COVERAGE

| Objective | Indicators | Why These Signals Matter |
|-----------|------------|--------------------------|
| Keep the narrator voice grounded so each choice continues to feel consequential, canonical, and emotionally consistent across branching beats. | author_coherence | This objective gives the doctor a named target for the narrative score so we can map dropped metaphors or inconsistent entities back to the health indicator before a story feels random. |
| Guard mutation payloads so any proposed scene commit is schema-valid and does not spin the graph into impossible states. | mutation_validity | The mutation validator ties this objective directly to graph constraints so operators see the fail cases, understand the log trace, and unblock corrupted playthroughs faster. |

---

## STATUS (RESULT INDICATOR)

```yaml
status:
  stream_destination: logs
  result:
    representation: score
    value: 0.98
    updated_at: 2025-12-20T10:10:00Z
    source: narrator_integration_test
```

---

## DOCK TYPES (COMPLETE LIST)

- `api` (input context)
- `graph_ops` (applied mutations)

---

## HOW TO USE THIS TEMPLATE

- Start by naming the flow and objective you intend to measure; the rest of the doc should hang from that navigation so downstream agents never have to guess which signal matters.
- Link indicators back to validation IDs in `VALIDATION_Narrator.md` and describe the dock types and cadence to make the check repeatable without rerunning the code search.
- Capture what each checker observes, how often the indicator is sampled, and any gap reminders in the same narrative length so the validator’s minimum-character guardrail never flags the doc.
- Once the health flow is defined, describe how to run the check in practice (integration test, CLI exercise, manual replay) so human operators can reproduce the runtime signal before blaming the doctor.

## CHECKER INDEX

```yaml
checkers:
  - name: schema_validator
    purpose: Ensure JSON output matches SceneTree and NarratorOutput.
    status: active
    priority: high
  - name: mutation_safety_checker
    purpose: Verify mutations don't violate graph constraints.
    status: active
    priority: high
```

---

## INDICATOR: author_coherence

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: author_coherence
  client_value: Ensures the story feels real and choices matter.
  validation:
    - validation_id: V1 (Narrator)
      criteria: Authorial intent preserved across turns.
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: narrator_input
    method: engine.infrastructure.orchestration.narrator.run_narrator
    location: engine/infrastructure/orchestration/narrator.py:50
  output:
    id: narrator_output
    method: engine.infrastructure.orchestration.narrator.run_narrator
    location: engine/infrastructure/orchestration/narrator.py:100
```

### HEALTH REPRESENTATION

```yaml
representation:
  allowed:
    - float_0_1
  selected:
    - float_0_1
semantics:
  float_0_1: Ratio of author-coherence passes versus total scene generations in the latest integration run.
  aggregation:
    method: Minimum-of-weighted-indicators so a single dropped connection drags the score instead of being averaged away.
    display: Surface the score through the narrator health banner and the doctor log so agents spot regressions quickly.
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Compare each streamed narrative chunk to the previous SceneTree state and the validation expectations so contradictory facts become immediate errors.
  steps:
    - Capture the narrator output from `NarratorService.generate` plus the persisted `mutations` payload.
    - Feed the narrative text and clickable metadata into the schema validator, confirming V1 and V4 invariants before the scene closes.
    - Flag the indicator if any entity changes diverge from the canonical graph, letting the doctor surface the mismatch as a logged failure.
  data_required: SceneTree narrative text, clickable metadata, mutated graph references, and the previous canon snapshot.
  failure_mode: The stream emits facts or character tones that do not align with the saved graph, so downstream scenes feel like different authors are writing.
```

## INDICATOR: mutation_validity

### VALUE TO CLIENTS & VALIDATION MAPPING

```yaml
value_and_validation:
  indicator: mutation_validity
  client_value: Prevents corrupted world state so future scenes reuse the same facts without surprises.
  validation:
    - validation_id: V3 (Narrator)
      criteria: Inventions persist as dedicated mutation batches before the narrator closes the scene.
    - validation_id: V6 (Narrator)
      criteria: Every mutation validates against the graph schema so downstream services accept the payload.
```

### HEALTH REPRESENTATION

```yaml
representation:
  allowed:
    - binary
    - float_0_1
  selected:
    - binary
semantics:
  binary: 1 if the latest mutation batch passed the schema & constraint checks, 0 otherwise.
aggregation:
  method: Logical AND of schema validator and mutation safety checks so a single violation fails the indicator.
  display: The doctor dashboard marks the narrator health as degraded when mutation_validity goes to zero so operators can pause scene release.
```

### DOCKS SELECTED

```yaml
docks:
  input:
    id: narrator_mutations
    method: engine.infrastructure.orchestration.narrator.NarratorService.generate
    location: engine/infrastructure/orchestration/narrator.py:27-110
  output:
    id: mutation_validation
    method: mutation_safety_checker
    location: docs/agents/narrator/HEALTH_Narrator.md#checker-index
```

### ALGORITHM / CHECK MECHANISM

```yaml
mechanism:
  summary: Run the mutation safety checker on every batch before confessing the scene, ensuring the graph remains consistent.
  steps:
    - Extract the `mutations` array from the narrator output and annotate it with the current scene ID.
    - Feed the annotations through `mutation_safety_checker`, which validates schema, referential integrity, and constraint compliance.
    - Emit a failure to the health log and mark the indicator as false if any mutation misses required fields or references invalid nodes.
  data_required: The mutation batch, the graph schema metadata, and the current scene identifier to contextualize the change.
  failure_mode: Mutations sneak past validation, leaving downstream services with inconsistent edges or nodes that cannot be rendered.
```

---

## HOW TO RUN

```bash
# Run narrator integration checks
pytest engine/tests/test_narrator_integration.py -v
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] Automated check for voice consistency across long threads so the narrator does not drift in tone during marathon play sessions.
- [ ] Hallucination detection for unprompted entity creation so unexpected characters or locations fail early instead of polluting the graph.
- [ ] Trigger a sanity run that compares narrator health scores with the CLI health banner to keep scoring aligned with human perception.
- [ ] Could we automatically diff every scene against the previous SceneTree so the doctor flags contradictions before the player notices?
- [ ] Explore instrumentation that correlates mutation_validity failures with the specific graph edges touched to speed up debugging.
- QUESTION: Should the health indicator include runtime telemetry from SSE logs so we can correlate latency spikes with schema violations?
