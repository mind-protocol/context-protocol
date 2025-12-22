# Tempo Controller — Sync: Current State

```
LAST_UPDATED: 2025-12-20
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Tempo is the pacing boundary between physics and canon surfacing.

**What's still being designed:**
- Exact interrupt definitions and player-link detection rules.

**What's proposed (v2+):**
- Adaptive pacing based on graph load.

---

## CURRENT STATE

Tempo documentation is established in this module chain, but no implementation
exists yet in the engine. Speed modes are defined by stop conditions rather
than fixed intervals.

---

## IN PROGRESS

### Tempo module scaffolding

- **Started:** 2025-12-20
- **By:** codex
- **Status:** in progress
- **Context:** Establish doc chain before wiring runtime.

---

## RECENT CHANGES

### 2025-12-20: Added tempo module docs

- **What:** Created PATTERNS/BEHAVIORS/ALGORITHM/VALIDATION/IMPLEMENTATION/HEALTH/SYNC docs.
- **Why:** Make the tempo loop a first-class module with explicit invariants.
- **Files:** docs/infrastructure/tempo/*
- **Struggles/Insights:** Kept scope narrow to pacing and surfacing boundaries.

---

## KNOWN ISSUES

### No implementation yet

- **Severity:** medium
- **Symptom:** Tempo loop does not exist in engine code.
- **Suspected cause:** Module was undocumented previously.
- **Attempted:** Doc chain only; no code changes.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement_Write_Or_Modify_Code

**Where I stopped:** Doc chain created; no runtime hooks.

**What you need to understand:**
Tempo is defined as the pacing loop that calls physics and canon without
blocking on narrator output. Implementation should live under
`engine/infrastructure/tempo/` and integrate with API endpoints.

**Watch out for:**
Avoid mixing narrator output with tempo surfacing. Tempo is timing only.

**Open questions I had:**
How to encode speed-to-interval mapping and backpressure thresholds.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Tempo is now a formal module in docs. Implementation is still pending.

**Decisions made:**
Tempo owns cadence and surfacing timing only, not content generation.

**Needs your input:**
Confirm desired speed intervals and per-tick surfacing caps.

---

## TODO

### Doc/Impl Drift

<!-- @ngram:todo DOCS→IMPL: Implement `engine/infrastructure/tempo/tempo_controller.py`. -->

### Tests to Run

```bash
ngram validate
```

### Immediate

<!-- @ngram:todo Create tempo controller loop in engine. -->
<!-- @ngram:todo Add API endpoints for speed and control. -->

### Later

<!-- @ngram:todo Add health checker implementation. -->
<!-- @ngram:proposition adaptive pacing based on queue size. -->

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Confident in scope, waiting for runtime integration decisions.

**Threads I was holding:**
Speed mapping, canon caps, and backpressure coupling.

**Intuitions:**
Tempo should remain simple; push complexity into physics and canon.

**What I wish I'd known at the start:**
How strict the pacing guarantees need to be for the UI.

---

## POINTERS

| What | Where |
|------|-------|
| Tempo algorithm | `docs/infrastructure/tempo/ALGORITHM_Tempo_Controller.md` |
| Tempo patterns | `docs/infrastructure/tempo/PATTERNS_Tempo.md` |
| Canon holder | `docs/infrastructure/canon/PATTERNS_Canon.md` |
