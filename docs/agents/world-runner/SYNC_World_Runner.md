# World Runner — Sync: Current State

```
STATUS: CANONICAL
UPDATED: 2025-12-20
```

## MATURITY

STATUS: CANONICAL

What's canonical (v1):
- World Runner orchestration, tick loop, and injection output are stable and fully implemented.
- Stateless operation via CLI is enforced.

## CURRENT STATE

The World Runner is complete. It operates as an adapter between the Python game engine and an AI agent that resolves off-screen narrative tensions.

## RECENT CHANGES

### 2025-12-31: Expand algorithm narrative and diagnostics

- **What:** Added extra prose to `ALGORITHM_World_Runner.md` describing how the objectives map to instrumentation, note-taking on `tick_trace`, and the strategy for `affects_player` so the doc now exceeds the template’s 50-character guidance everywhere.
- **Why:** DOC_TEMPLATE_DRIFT singled out the algorithm for missing objective narratives and short sections; the new paragraphs and bullet support ensure each function heading explains why the Runner behaves the way it does before showing code.
- **Files:** `docs/agents/world-runner/ALGORITHM_World_Runner.md`, `docs/agents/world-runner/SYNC_World_Runner.md`
- **Verification:** `ngram validate` *(still fails for the known connectome/health module, membrane naming, and CHAIN warnings already tracked elsewhere)*.

### 2026-01-02: Fill PATTERNS template coverage

- **What:** Added the missing PATTERNS sections (behaviors supported/prevented, principles, data, dependencies, inspirations, scope, and gaps) with 50+ character narratives so the template warning is satisfied.
- **Why:** DOC_TEMPLATE_DRIFT reported `PATTERNS_World_Runner.md` as missing the required sections and short on narrative length, so this change keeps the canonical rationale authoritative without touching runtime behavior.
- **Files:** `docs/agents/world-runner/PATTERNS_World_Runner.md`, `docs/agents/world-runner/SYNC_World_Runner.md`
- **Verification:** `ngram validate`

### 2025-12-21: Expand health template coverage

- **What:** Completely rebuilt `HEALTH_World_Runner.md` so every required template section (purpose, why, flows, objectives, indicators, docks, checkers, instructions, gaps, and ideas) now exists with 50+ character prose.
- **Why:** DOC_TEMPLATE_DRIFT flagged the health document for missing the new template sections, so the rewrite keeps the health ledger compliant while leaving runtime behavior untouched.
- **Files:** `docs/agents/world-runner/HEALTH_World_Runner.md`, `docs/agents/world-runner/SYNC_World_Runner.md`, `.ngram/state/SYNC_Project_State.md`
- **Verification:** `ngram validate`

### 2025-12-21: Expand implementation doc template coverage

- **What:** Added explicit `LOGIC CHAINS`, `RUNTIME BEHAVIOR`, `CONFIGURATION`, `BIDIRECTIONAL LINKS`, and `GAPS / IDEAS / QUESTIONS` sections to the World Runner implementation doc so every required template block exceeds the length threshold.
- **Why:** DOC_TEMPLATE_DRIFT for `IMPLEMENTATION_World_Runner_Service_Architecture.md` reported the missing sections, so we enriched the prose while keeping the runtime behavior unchanged.
- **Files:** `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md`, `docs/agents/world-runner/SYNC_World_Runner.md`
- **Verification:** `ngram validate`

### 2025-12-21: Align runner algorithm doc with template

- **What:** Added the missing `OBJECTIVES AND BEHAVIORS` block, expanded the `run_world` narrative, and documented `affects_player` under the canonical `ALGORITHM: {function name}` headings so template compliance is restored.
- **Why:** DOC_TEMPLATE_DRIFT reported `ALGORITHM_World_Runner.md` as missing required sections/function descriptions, so filling them keeps the canonical chain explicit without touching runtime code.
- **Files:** `docs/agents/world-runner/ALGORITHM_World_Runner.md`
- **Verification:** `ngram validate`

### 2025-12-31: Polish algorithm objectives coverage

- **What:** Replaced the short objectives table in `ALGORITHM_World_Runner.md` with three behavior-driven objectives, each with narrative descriptions exceeding the template's 50-character floor.
- **Why:** The DOC_TEMPLATE_DRIFT warning still flagged this algorithm doc because the original rows were too terse; expanding them satisfies the length requirement while keeping the runner goals explicit.
- **Impact:** The canonical algorithm now explicitly ties interrupt/completion guarantees to runner behavior, so downstream agents understand the contract each invocation fulfills before touching execution logic.

### 2025-12-31: Complete health template coverage

- **What:** Rebuilt `HEALTH_World_Runner.md` so every template section (purpose, why, objective table, flows, indicators, docks, checkers, indicator narratives, known gaps, and ideas) is present with 50+ character narratives.
- **Why:** DOC_TEMPLATE_DRIFT flagged the health doc as missing key sections, so this rewrite ensures the World Runner health coverage now matches the template without changing runtime checks.
- **Files:** `docs/agents/world-runner/HEALTH_World_Runner.md`, `docs/agents/world-runner/SYNC_World_Runner.md`
- **Verification:** `ngram validate`

### 2025-12-21: Expand validation template coverage

- **What:** Expanded `VALIDATION_World_Runner_Invariants.md` with BEHAVIORS GUARANTEED and OBJECTIVES COVERED tables plus a HEALTH COVERAGE section that call out the new long-form guarantees, tie each objective to the runner invariants, and surface `background_consistency`, `adapter_resilience`, and the fallback checks in `HEALTH_World_Runner.md`.
- **Why:** The DOC_TEMPLATE_DRIFT warning reported those validation template blocks missing or too terse; this repair keeps the canonical ledger compliant while documenting why each behavior matters for the health indicators and how operators can triage the error modes.
- **Files:** `docs/agents/world-runner/VALIDATION_World_Runner_Invariants.md`, `docs/agents/world-runner/SYNC_World_Runner.md`
- **Verification:** `ngram validate`

### 2025-12-20: Ngram Framework Refactor

- **What:** Refactored `IMPLEMENTATION_World_Runner_Service_Architecture.md` and updated `TEST_World_Runner_Coverage.md` to the Health format.
- **Why:** To align with the new ngram documentation standards and emphasize DATA FLOW AND DOCKING.
- **Impact:** World Runner documentation is now compliant; Health checks are anchored to the CLI adapter boundary.

## HANDOFF: FOR AGENTS

Use VIEW_Implement_Write_Or_Modify_Code for adapter changes. Ensure any changes to the agent's instructions in `CLAUDE.md` are reflected in the Health indicators.

## IN PROGRESS

No active implementation work is underway right now; all core logic is considered stable and any future updates will follow the existing VIEW guidance and the CLI/AI contract described elsewhere.

## KNOWN ISSUES

- None outstanding; the orchestration loop is stable, but keep an eye on upstream engine schema changes and injection payload expectations whenever a larger refactor touches the narrator-state boundaries.

## HANDOFF: FOR HUMAN

Please confirm any decision to validate the injection schema or extend the CLI adapter before asking another agent to modify this module, and note that the DOC_TEMPLATE_DRIFT warning for this SYNC has been satisfied.

## TODO

- [ ] Add unit tests for `WorldRunnerService` fallback behaviors.
- [ ] Implement automated schema validation for injection payloads.

## POINTERS

- `docs/agents/world-runner/PATTERNS_World_Runner.md` for the core "own time" insight.
- `docs/agents/world-runner/IMPLEMENTATION_World_Runner_Service_Architecture.md` for adapter details.

## CHAIN

```
THIS:            SYNC_World_Runner.md (you are here)
PATTERNS:        ./PATTERNS_World_Runner.md
BEHAVIORS:       ./BEHAVIORS_World_Runner.md
ALGORITHM:       ./ALGORITHM_World_Runner.md
VALIDATION:      ./VALIDATION_World_Runner_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_World_Runner_Service_Architecture.md
TEST:            ./TEST_World_Runner_Coverage.md
```

## CONSCIOUSNESS TRACE

**Momentum:** The pipeline is calm; stability has returned to the adapter, and the lingering template warning for this SYNC is now closed.

**Architectural concerns:** Overwriting the CLI/agent contract would risk drift, so any future work must make those dependencies explicit before touching the Runner.

**Opportunities noticed:** This doc can serve as the handoff anchor for any future automation on the injection schema health checks.
