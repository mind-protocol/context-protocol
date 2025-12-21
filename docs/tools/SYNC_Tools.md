# Tools — Sync: Current State

```
LAST_UPDATED: 2025-12-21
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Tools.md
BEHAVIORS:       ./BEHAVIORS_Tools.md
ALGORITHM:       ./ALGORITHM_Tools.md
VALIDATION:      ./VALIDATION_Tools.md
IMPLEMENTATION:  ./IMPLEMENTATION_Tools.md
HEALTH:          ./HEALTH_Tools.md
THIS:            ./SYNC_Tools.md
```

---

## CURRENT STATE

Documented the tools module so utility scripts are tracked in the protocol.
Added systemd user unit templates under `tools/systemd/user/`, a v3 ngrok
config at `tools/ngrok.yml`, and a WSL autostart guide at
`docs/infrastructure/wsl-autostart.md`. Added `.ngram/logs/` plus a
`.ngram/systemd.env` placeholder to wire frontend commands into systemd.
Added `blood-fe.service` to run the `the-blood-ledger` frontend and wired it
into `ngram-stack.target`.
Expanded `docs/tools/VALIDATION_Tools.md` so the validation template now
includes behaviors guaranteed, objectives covered, properties, error
conditions, health coverage, verification procedures, sync status, and gap
analysis narratives that each exceed the 50-character guidance. Expedited
`docs/tools/ALGORITHM_Tools.md` so the algorithm ledger now highlights the
bundle splitter, dialogue streamer, and stack runner flows through overview,
objectives, data structures, algorithm callouts, decisions, data flow,
complexity, helper functions, interactions, and gaps sections so future agents
see how those helpers satisfy the protocol template requirements. Expanded
`docs/tools/HEALTH_Tools.md` so the health ledger now lists PURPOSE OF THIS
FILE, WHY THIS PATTERN, FLOWS ANALYSIS, HEALTH INDICATORS, OBJECTIVES,
STATUS, DOCK TYPES, CHECKER INDEX, indicator narratives, HOW TO RUN guidance,
and GAPS/IDEAS/QUESTIONS narratives that each exceed 50 characters. Expanded
`docs/tools/BEHAVIORS_Tools.md` so the behavior ledger now includes OBJECTIVES
SERVED, INPUTS / OUTPUTS, EDGE CASES, ANTI-BEHAVIORS, and GAPS / IDEAS /
QUESTIONS sections with 50+ character narratives describing the splitter,
streaming events, and helper contracts while linking each section back to the
tools module flows.
Bolstered `docs/tools/BEHAVIORS_Tools.md` so it now calls out OBJECTIVES
SERVED, INPUTS / OUTPUTS, EDGE CASES, ANTI-BEHAVIORS, and GAPS / IDEAS /
QUESTIONS with descriptive prose that anchors B1 and B2 in the module scope.
Documented that `tools/run_stack.sh` logs each service restart to `./logs/run_stack`
and appends stderr to `./.ngram/error.log`, matching the new OUTPUTS (stack runner)
memo in the behavior ledger.

Expanded `docs/tools/IMPLEMENTATION_Tools.md` from a short code-location list into the full template so CODE STRUCTURE, DESIGN PATTERNS, SCHEMA, ENTRY POINTS, DATA FLOWS, LOGIC CHAINS, MODULE DEPENDENCIES, STATE MANAGEMENT, RUNTIME BEHAVIOR, CONCURRENCY MODEL, CONFIGURATION, BIDIRECTIONAL LINKS, and GAPS sections all now exceed the 50-character threshold while covering the bundle splitter, stream helper, and stack orchestrator.

## Agent Observations

### Remarks
- No frontend start command exists in-repo; `ngram-fe.service` now requires
  `FE_CMD` in `.ngram/systemd.env`.
- `ngram-fe.service` now targets `~/ngram/frontend`; the blood frontend has its
  own unit.
- The updated ALGORITHM doc now narrates how the bundle splitter, the narrator
  stream, and the helper stack interact so DOC_TEMPLATE_DRIFT warnings are kept
  in check on this module.
- The algorithm doc now explicitly lists overview, objectives, decisions, data flow, helper functions, interactions, and gaps so future agents can trace its behavior story before touching the splitter or streamer.
- The algorithm doc now explicitly calls out its overview, objectives, key
  decisions, data flow, helper functions, interactions, and gaps so every future
  agent can trace the behavior story before touching the splitter or streamer.
- The HEALTH doc now records flows, indicator coverage, and the checker index
  so DOC_TEMPLATE_DRIFT guardrails are satisfied for this module.
- `docs/tools/ALGORITHM_Tools.md` now calls out overview, objectives, structures,
  helper functions, and interactions so future agents can trace behavior to the
  underlying scripts before touching the splitter or streamer.
- `docs/tools/IMPLEMENTATION_Tools.md` now narrates the required code structure,
  design patterns, schema, flow, dependencies, runtime behavior, concurrency,
  and configuration sections so the implementation ledger no longer lags the
  rest of the module documentation.

### Suggestions
- [ ] Confirm the exact frontend start command and update
  `.ngram/systemd.env` so `ngram-fe.service` can start cleanly.
- [ ] Confirm the blood frontend port/command once its build is finalized.
- [ ] Add `# DOCS: docs/tools/IMPLEMENTATION_Tools.md` comments to `tools/connectome_doc_bundle_splitter_and_fence_rewriter.py`, `tools/stream_dialogue.py`, and `tools/run_stack.sh` so the implementation narrative is reachable from the scripts.

### Propositions
- If a canonical frontend repo exists, add a brief doc link here so future
  agents can locate its startup command quickly.

## TODO

- [ ] Add fixtures and run examples for each script to validate outputs.
- [ ] Create CI-friendly fixtures for the splitter and stream helper so the missing implementation checklist items can be automated.

## RECENT CHANGES

### 2026-01-26: Document tools pattern template coverage

- **What:** Added the missing BEHAVIORS SUPPORTED, BEHAVIORS PREVENTED, PRINCIPLES, DATA, DEPENDENCIES, INSPIRATIONS, SCOPE, and GAPS / IDEAS / QUESTIONS sections to `docs/tools/PATTERNS_Tools.md` so every required PATTERN block now exceeds the 50-character threshold and captures the guardrails for the helper scripts.
- **Why:** DOC_TEMPLATE_DRIFT flagged those PATTERN sections as missing or too brief, so the expanded prose now records the intent, data dependencies, and risks that justify the tools module without touching application code.
- **Files:** `docs/tools/PATTERNS_Tools.md`, `docs/tools/SYNC_Tools.md`
- **Verification:** `ngram validate` *(fails for the known docs/connectome/health PATTERNS/SYNC gaps, the `docs/engine/membrane` PATTERN naming mismatch, and the longstanding CHAIN/link warnings).*

### 2026-01-16: Complete tools implementation template coverage

- **What:** Expanded `docs/tools/IMPLEMENTATION_Tools.md` to capture the module tree, design patterns, schema, entry points, data flows, logic chains, dependencies, state management, runtime behavior, concurrency model, configuration, bidirectional links, and open gaps while calling out the bundle splitter, stream dialogue helper, and stack orchestrator.
- **Why:** DOC_TEMPLATE_DRIFT flagged this implementation doc for missing CODE STRUCTURE, DESIGN PATTERNS, SCHEMA, ENTRY POINTS, DATA FLOW, LOGIC CHAINS, MODULE DEPENDENCIES, STATE MANAGEMENT, RUNTIME BEHAVIOR, CONCURRENCY MODEL, CONFIGURATION, BIDIRECTIONAL LINKS, and GAPS sections, so the rewrite restores the canonical coverage.
- **Files:** `docs/tools/IMPLEMENTATION_Tools.md`, `docs/tools/SYNC_Tools.md`
- **Verification:** `ngram validate` *(fails for the existing docs/connectome/health PATTERNS/SYNC gaps, the `docs/engine/membrane` PATTERN naming mismatch, and the longstanding CHAIN/link warnings).*

### 2026-01-27: Complete tools sync template coverage

- **What:** Added MATURITY, IN PROGRESS, KNOWN ISSUES, HANDOFFS, CONSCIOUSNESS TRACE, and POINTERS sections to `docs/tools/SYNC_Tools.md` so every required block now exceeds fifty characters and clearly states the runtime context without touching the helper scripts.
- **Why:** DOC_TEMPLATE_DRIFT flagged the tools SYNC template for missing sections, so the expanded narrative keeps the state ledger traceable while leaving runtime helpers untouched.
- **Files:** `docs/tools/SYNC_Tools.md`, `.ngram/state/SYNC_Project_State.md`
- **Verification:** `ngram validate` *(fails: known docs/connectome/health PATTERNS/SYNC gaps, `docs/engine/membrane/PATTERN_Membrane_Modulation.md` naming mismatch, and existing CHAIN/link warnings).*

### 2025-12-21: Expand tools algorithm template coverage

- **What:** Filled the missing overview, objectives, data structures, algorithm
  callout, key decisions, data flow, complexity, helper functions, interactions,
  and gaps sections in `docs/tools/ALGORITHM_Tools.md` so every block exceeds
  50 characters and ties the bundle splitter, narrator streamer, and stack runner
  flows back to the behavior ledger.
- **Why:** DOC_TEMPLATE_DRIFT flagged the algorithm doc for missing template
  blocks, so this update keeps the module ledger authoritative without touching
  the runtime utilities.
- **Files:** `docs/tools/ALGORITHM_Tools.md`, `docs/tools/SYNC_Tools.md`
- **Verification:** `ngram validate` *(fails: the known
  docs/connectome/health PATTERNS/SYNC gaps, the engine/membrane PATTERN naming
  mismatch, and the existing CHAIN/link warnings).*

- **What:** Added the missing OBJECTIVES SERVED, INPUTS / OUTPUTS, EDGE CASES,
  ANTI-BEHAVIORS, and GAPS / IDEAS / QUESTIONS sections to
  `docs/tools/BEHAVIORS_Tools.md`, expanded B1/B2 narratives so each block now
  exceeds 50 characters, and noted the addition in the module sync.
- **Why:** DOC_TEMPLATE_DRIFT flagged the behaviors doc for missing template
  sections, so the expanded prose keeps the ledger aligned without touching the
  helper scripts themselves.
- **Files:** `docs/tools/BEHAVIORS_Tools.md`, `docs/tools/SYNC_Tools.md`
- **Verification:** `ngram validate` *(fails: the existing
  docs/connectome/health PATTERNS/SYNC gaps, the `docs/engine/membrane`
  PATTERN naming mismatch, and the longstanding CHAIN/link warnings already
  reported by the doctor).*

### 2026-01-13: Document tools algorithm template coverage

- **What:** Added the missing overview, objectives, data structures, algorithm
  callout, key decisions, data flow, complexity, helper functions, interactions,
  and gaps sections to `docs/tools/ALGORITHM_Tools.md`, giving each block more
  than 50 characters and tying the narrative back to the bundle splitter and
  stream dialogue helpers.
- **Why:** DOC_TEMPLATE_DRIFT flagged `docs/tools/ALGORITHM_Tools.md` for
  omitting the required sections, so the new narrative keeps the module
  compliant without touching the scripts themselves.
- **Files:** `docs/tools/ALGORITHM_Tools.md`, `docs/tools/SYNC_Tools.md`
- **Verification:** `ngram validate` *(fails for the known
  docs/connectome/health PATTERNS/SYNC gaps, the engine/membrane PATTERN
  naming mismatch, and the existing CHAIN/link warnings).*

### 2026-01-15: Expand tools behaviors template coverage

- **What:** Added robust OBJECTIVES SERVED, INPUTS / OUTPUTS, EDGE CASES,
  ANTI-BEHAVIORS, and GAPS / IDEAS / QUESTIONS sections to
  `docs/tools/BEHAVIORS_Tools.md`, each exceeding 50 characters and explaining
  how the splitter and streamer guard the documentation/streaming experience.
- **Why:** DOC_TEMPLATE_DRIFT reported these sections missing or too brief, so
  the expanded prose now makes the behavior contract explicit without modifying
  runtime scripts.
- **Files:** `docs/tools/BEHAVIORS_Tools.md`, `docs/tools/SYNC_Tools.md`
- **Verification:** `ngram validate` *(fails for the known
  docs/connectome/health PATTERNS/SYNC gaps, the engine/membrane PATTERN
  naming mismatch, and the existing CHAIN/link warnings).*

### 2026-01-15: Document tools implementation template coverage

- **What:** Expanded `docs/tools/IMPLEMENTATION_Tools.md` to describe the code
  structure, design patterns, schema, entry points, flow-by-flow docking, logic
  chains, module dependencies, state management, runtime behavior, concurrency
  model, configuration, bidirectional links, and gaps list so every blocking
  section meets the template criteria while leaving the helper scripts untouched.
- **Why:** DOC_TEMPLATE_DRIFT flagged `docs/tools/IMPLEMENTATION_Tools.md` for
  lacking those sections, so the new narrative keeps the ledger compliant without
  modifying the runtime helpers.
- **Files:** `docs/tools/IMPLEMENTATION_Tools.md`, `docs/tools/SYNC_Tools.md`
- **Verification:** `ngram validate` *(fails for the known
  docs/connectome/health PATTERNS/SYNC gaps, the engine/membrane PATTERN
  naming mismatch, and the existing CHAIN/link warnings).*

### 2026-01-05: Document tools validation template coverage

- **What:** Filled `docs/tools/VALIDATION_Tools.md` with the missing validation sections (behaviors guaranteed, objectives covered, properties, error conditions, health coverage, verification procedures, sync status, and gaps/ideas/questions) so every template block now meets the 50+ character expectation.
- **Why:** DOC_TEMPLATE_DRIFT warned that the validation template lacked the required narrative anchors, so this update keeps the canonical ledger authoritative without modifying the runtime scripts.
- **Files:** `docs/tools/VALIDATION_Tools.md`, `docs/tools/SYNC_Tools.md`
- **Verification:** `ngram validate` *(fails for the known docs/connectome/health PATTERNS/SYNC gaps, the engine/membrane PATTERN naming mismatch, and the existing CHAIN/link warnings).)*

### 2025-12-21: Expand tools algorithm template coverage

- **What:** Filled `docs/tools/ALGORITHM_Tools.md` with the missing overview, objectives, data structure, function-level, and interaction sections so every template block now exceeds the 50-character guidance.
- **Why:** DOC_TEMPLATE_DRIFT flagged the algorithm doc for lacking the required subsections, so this change keeps the module's narrative aligned with the rest of the protocol without touching the scripts themselves.
- **Files:** `docs/tools/ALGORITHM_Tools.md`, `docs/tools/SYNC_Tools.md`
- **Verification:** `ngram validate` *(fails for the known docs/connectome/health PATTERNS/SYNC gaps, the engine/membrane PATTERN naming mismatch, and the existing CHAIN/link warnings).)*
