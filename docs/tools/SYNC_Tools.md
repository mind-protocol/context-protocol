# Tools — Sync: Current State

```
LAST_UPDATED: 2026-01-27
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

## MATURITY

STATUS: DESIGNING

What's canonical (v1):
- The tools module now centralizes documentation helpers, stack rerunners, and streaming adapters, so these utilities stay under a single narrative while their instrumentation is still maturing.
- Responsibility for every helper script now includes doc template coverage, so every edit must keep the narrative, behaviors, and implementation chains aligned before we call this module canonical.

What's still being designed:
- The front-end start command, ngrok defaults, and stack restart orchestration continue to evolve, so the tools module remains in designing status until those flows stabilize.

## CURRENT STATE

Documented the tools module so utility scripts are tracked in the protocol and so the doc templates, streaming helpers, and stack restart assistants share a single canonical narrative. Added systemd user unit templates under `tools/systemd/user/`, a v3 ngrok config at `tools/ngrok.yml`, and a WSL autostart guide at `docs/infrastructure/wsl-autostart.md`. Added `.ngram/logs/` plus the `.ngram/systemd.env` placeholder to wire frontend commands into systemd, documented the blood-fe service wiring and `ngram-stack.target`, captured the `tools/run_stack.sh` logging behavior, and expanded the algorithm, validation, health, and behaviors docs so the entire chain satisfies the DOC_TEMPLATE_DRIFT narrative requirements while the implementation ledger tracks the required logic chains.
This sync now explicitly mentions the run_stack restart context so the Implementation ledger traces the same operations the doc describes, keeping the canonical chain auditable when the helpers get refactored.

## IN PROGRESS

Steady verification that the expanded documentation chain now passes DOC_TEMPLATE_DRIFT while the helper scripts continue to satisfy their described behaviors, the front-end start commands finish their final pathing, and the ngrok runner honors the planned environment variables.

## KNOWN ISSUES

- The front-end start command remains undefined in `.ngram/systemd.env`, so `ngram-fe.service` cannot yet start the expected process without confirmation of the canonical command string.
- The ngrok helper still assumes environment variables that are only described in high-level guides, which makes local runs brittle until the `.env` template is verified by someone with access to the production config.

## RECENT CHANGES

### 2026-01-27: Complete tools sync template coverage

- **What:** Added MATURITY, IN PROGRESS, KNOWN ISSUES, HANDOFFS, CONSCIOUSNESS TRACE, and POINTERS sections to `docs/tools/SYNC_Tools.md` so every required block now exceeds fifty characters, the ledger records the new template expectations, and the module state is explicit for downstream agents.
- **Why:** DOC_TEMPLATE_DRIFT flagged this sync file for missing those sections, so the richer narrative keeps the state ledger traceable while leaving the helper scripts untouched.
- **Files:** `docs/tools/SYNC_Tools.md`, `.ngram/state/SYNC_Project_State.md`
- **Verification:** `ngram validate` *(fails: known docs/connectome/health PATTERNS/SYNC gaps, `docs/engine/membrane/PATTERN_Membrane_Modulation.md` naming mismatch, and existing CHAIN/link warnings).* 

### 2026-01-15: Complete tools behavior template coverage

- **What:** Added the missing OBJECTIVES SERVED, INPUTS / OUTPUTS, EDGE CASES, ANTI-BEHAVIORS, and GAPS / IDEAS / QUESTIONS sections to `docs/tools/BEHAVIORS_Tools.md`, expanded B1/B2 narratives so each block now exceeds 50 characters, and noted the addition in the module sync.
- **Why:** DOC_TEMPLATE_DRIFT flagged the behaviors doc for missing template sections, so the expanded prose keeps the ledger aligned without touching the helper scripts themselves.
- **Files:** `docs/tools/BEHAVIORS_Tools.md`, `docs/tools/SYNC_Tools.md`
- **Verification:** `ngram validate` *(fails: the existing docs/connectome/health PATTERNS/SYNC gaps, the `docs/engine/membrane` PATTERN naming mismatch, and the longstanding CHAIN/link warnings already reported by the doctor).* 

### 2026-01-13: Document tools algorithm template coverage

- **What:** Added the missing overview, objectives, data structures, algorithm callout, key decisions, data flow, complexity, helper functions, interactions, and gaps sections to `docs/tools/ALGORITHM_Tools.md`, giving each block more than 50 characters and tying the narrative back to the bundle splitter and stream dialogue helpers.
- **Why:** DOC_TEMPLATE_DRIFT flagged `docs/tools/ALGORITHM_Tools.md` for omitting the required sections, so the new narrative keeps the module compliant without touching the scripts themselves.
- **Files:** `docs/tools/ALGORITHM_Tools.md`, `docs/tools/SYNC_Tools.md`
- **Verification:** `ngram validate` *(fails for the known docs/connectome/health PATTERNS/SYNC gaps, the engine/membrane PATTERN naming mismatch, and the existing CHAIN/link warnings).* 

### 2026-01-15: Expand tools behaviors template coverage

- **What:** Added robust OBJECTIVES SERVED, INPUTS / OUTPUTS, EDGE CASES, ANTI-BEHAVIORS, and GAPS / IDEAS / QUESTIONS sections to `docs/tools/BEHAVIORS_Tools.md`, each exceeding 50 characters and explaining how the splitter and streamer guard the documentation/streaming experience.
- **Why:** DOC_TEMPLATE_DRIFT reported these sections missing or too brief, so the expanded prose now makes the behavior contract explicit without modifying runtime scripts.
- **Files:** `docs/tools/BEHAVIORS_Tools.md`, `docs/tools/SYNC_Tools.md`
- **Verification:** `ngram validate` *(fails for the known docs/connectome/health PATTERNS/SYNC gaps, the engine/membrane PATTERN naming mismatch, and the existing CHAIN/link warnings).* 

### 2026-01-15: Document tools implementation template coverage

- **What:** Expanded `docs/tools/IMPLEMENTATION_Tools.md` to describe the code structure, design patterns, schema, entry points, flow-by-flow docking, logic chains, module dependencies, state management, runtime behavior, concurrency model, configuration, bidirectional links, and gaps list so every blocking section meets the template criteria while leaving the helper scripts untouched.
- **Why:** DOC_TEMPLATE_DRIFT flagged `docs/tools/IMPLEMENTATION_Tools.md` for lacking those sections, so the new narrative keeps the ledger compliant without modifying the runtime helpers.
- **Files:** `docs/tools/IMPLEMENTATION_Tools.md`, `docs/tools/SYNC_Tools.md`
- **Verification:** `ngram validate` *(fails for the known docs/connectome/health PATTERNS/SYNC gaps, the engine/membrane PATTERN naming mismatch, and the existing CHAIN/link warnings).* 

### 2026-01-05: Document tools validation template coverage

- **What:** Filled `docs/tools/VALIDATION_Tools.md` with the missing validation sections (behaviors guaranteed, objectives covered, properties, error conditions, health coverage, verification procedures, sync status, and gaps/ideas/questions) so every template block now meets the 50+ character expectation.
- **Why:** DOC_TEMPLATE_DRIFT warned that the validation template lacked the required narrative anchors, so this update keeps the canonical ledger authoritative without modifying the runtime scripts.
- **Files:** `docs/tools/VALIDATION_Tools.md`, `docs/tools/SYNC_Tools.md`
- **Verification:** `ngram validate` *(fails for the known docs/connectome/health PATTERNS/SYNC gaps, the engine/membrane PATTERN naming mismatch, and the existing CHAIN/link warnings).)* 

## Agent Observations

### Remarks
- Added MATURITY, IN PROGRESS, KNOWN ISSUES, HANDOFF, CONSCIOUSNESS TRACE, and POINTERS narratives so the tools sync file finally records the expected template sections for agents and humans to reference.
- No frontend start command exists in-repo; `ngram-fe.service` now requires `FE_CMD` in `.ngram/systemd.env`.
- `ngram-fe.service` now targets `~/ngram/frontend`; the blood frontend has its own unit.
- The updated ALGORITHM doc now narrates how the bundle splitter, the narrator stream, and the helper stack interact so DOC_TEMPLATE_DRIFT warnings are kept in check on this module.
- The HEALTH doc now records flows, indicator coverage, and the checker index so DOC_TEMPLATE_DRIFT guardrails are satisfied for this module.
- `docs/tools/IMPLEMENTATION_Tools.md` now narrates the required code structure, design patterns, schema, flow, dependencies, runtime behavior, concurrency, and configuration sections so the implementation ledger no longer lags the rest of the module documentation.

### Suggestions
- [ ] Confirm the exact frontend start command and update `.ngram/systemd.env` so `ngram-fe.service` can start cleanly.
- [ ] Confirm the blood frontend port/command once its build is finalized.
- [ ] Add `# DOCS: docs/tools/IMPLEMENTATION_Tools.md` comments to `tools/connectome_doc_bundle_splitter_and_fence_rewriter.py`, `tools/stream_dialogue.py`, and `tools/run_stack.sh` so the implementation narrative is reachable from the scripts.

### Propositions
- If a canonical frontend repo exists, add a brief doc link here so future agents can locate its startup command quickly.

## TODO

- [ ] Add fixtures and run examples for each script to validate outputs.
- [ ] Create CI-friendly fixtures for the splitter and stream helper so the missing implementation checklist items can be automated.

## HANDOFF: FOR AGENTS

Use `VIEW_Implement_Write_Or_Modify_Code.md` for future work on this module, and keep in mind that every doc change must also refresh the DOC_TEMPLATE_DRIFT checklist so the next agent inherits a fully stated sync.

## HANDOFF: FOR HUMAN

Please confirm the canonical front-end start command, the blood frontend port/command, and the ngrok environment defaults before another agent considers the module ready for canonical status.

## POINTERS

- `docs/tools/IMPLEMENTATION_Tools.md` for the code architecture, entry points, and stack runner wiring that this sync now references explicitly.
- `docs/tools/HEALTH_Tools.md` for the flows, indicators, and checkers that validate the helper scripts and connect to this module's behavior and validation narratives.
- `docs/tools/BEHAVIORS_Tools.md` for the updated behavior ledger, including the OUTPUTS (stack runner) note describing which `tools/run_stack.sh` restarts wrote to `./logs/run_stack` and `./.ngram/error.log`.

## CONSCIOUSNESS TRACE

**Momentum:** Documented the helper scripts, systemd wiring, and doc templates so the module can track DOC_TEMPLATE_DRIFT compliance and queue future automation around the stack runner flow.

**Architectural concerns:** Systemd wiring, frontend commands, and ngrok config remain loosely tied to ad-hoc env vars, so avoid scattering those details across multiple sources before stabilizing the values.

**Opportunities noticed:** This sync file now models how docs, behaviors, algorithms, validation, and health indicators interlock; future agents can copy this structure when expanding the stack scripts or adding new helpers.
