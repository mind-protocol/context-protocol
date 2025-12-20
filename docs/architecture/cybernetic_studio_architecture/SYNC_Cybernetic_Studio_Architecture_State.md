# Cybernetic Studio Architecture — Sync: Current State

```
LAST_UPDATED: 2025-12-20
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Cybernetic_Studio_Architecture.md
BEHAVIORS:       ./BEHAVIORS_Cybernetic_Studio_System_Behaviors.md
ALGORITHM:       ./ALGORITHM_Cybernetic_Studio_Process_Flow.md
VALIDATION:      ./VALIDATION_Cybernetic_Studio_Architectural_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Cybernetic_Studio_Code_Structure.md
HEALTH:          ./HEALTH_Cybernetic_Studio_Health_Checks.md
THIS:            SYNC_Cybernetic_Studio_Architecture_State.md (you are here)

IMPL:            N/A (Conceptual Architecture Document)
SOURCE:          ../../../data/ARCHITECTURE — Cybernetic Studio.md
```

---

## MATURITY

**What's canonical (v1):**
- Two-repo topology (`ngram` platform + `blood-ledger` cartridge) with shared graph service.
- Repo artifacts are source of truth; graph stores meaning via EvidenceRefs.
- Places (SYNC/UI/VIEW) are first-class surfaces.

**What's still being designed:**
- Weight evolution rules and pruning policy.
- Canonization policy for dev narratives vs local moments.
- EvidenceRef schema details (string vs structured object).

**What's proposed (v2+):**
- Extract `graph-physics-core` if platform entanglement becomes painful.

---

## CURRENT STATE

The Cybernetic Studio architecture docs are now a full chain (PATTERNS → BEHAVIORS → ALGORITHM → VALIDATION → IMPLEMENTATION → HEALTH → SYNC) sourced from the raw architecture file in `data/ARCHITECTURE — Cybernetic Studio.md`. Implementation is still conceptual; no runtime wiring or health checks exist yet.

---

## IN PROGRESS

### Architecture Doc Chain Completion

- **Started:** 2025-12-20
- **By:** codex
- **Status:** complete (documentation only)
- **Context:** Fill missing chain docs and connect external implementation plans.

---

## RECENT CHANGES

### 2025-12-20: Completed Cybernetic Studio doc chain

- **What:** Added ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH, and SYNC docs.
- **Why:** The architecture chain referenced these docs but they did not exist.
- **Files:** `docs/architecture/cybernetic_studio_architecture/ALGORITHM_Cybernetic_Studio_Process_Flow.md`, `docs/architecture/cybernetic_studio_architecture/VALIDATION_Cybernetic_Studio_Architectural_Invariants.md`, `docs/architecture/cybernetic_studio_architecture/IMPLEMENTATION_Cybernetic_Studio_Code_Structure.md`, `docs/architecture/cybernetic_studio_architecture/HEALTH_Cybernetic_Studio_Health_Checks.md`, `docs/architecture/cybernetic_studio_architecture/SYNC_Cybernetic_Studio_Architecture_State.md`
- **Struggles/Insights:** Kept implementation conceptual and pointed to the async implementation plan in `blood-ledger` rather than duplicating it.

### 2025-12-20: Added missing CHAIN block to SYNC doc

- **What:** Linked the full doc chain in this SYNC file.
- **Why:** Fixes INCOMPLETE_CHAIN and keeps the chain bidirectional.
- **Files:** `docs/architecture/cybernetic_studio_architecture/SYNC_Cybernetic_Studio_Architecture_State.md`

---

## KNOWN ISSUES

### No runtime verification

- **Severity:** low
- **Symptom:** Health checks and validation are documentation-only.
- **Suspected cause:** Graph hooks and watchers are not implemented yet.
- **Attempted:** Documented intended docks and pending checkers.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement_Write_Or_Modify_Code

**Where I stopped:** Completed the Cybernetic Studio doc chain and referenced the external async plan.

**What you need to understand:**
Implementation details are still conceptual; use the external plan in `blood-ledger` for async wiring guidance.

**Watch out for:**
Do not add parallel architecture docs; extend this chain instead.

**Open questions I had:**
Where should the Place registry live: in `ngram` or in the graph service?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Completed the missing Cybernetic Studio doc chain and linked the external async implementation plan from `blood-ledger`. No runtime code changes were made.

**Decisions made:**
Kept implementation sections conceptual and avoided duplicating the async plan.

**Needs your input:**
Confirm whether the async plan should be mirrored into ngram docs or kept as a cross-repo pointer.

---

## TODO

### Doc/Impl Drift

- [ ] IMPL→DOCS: Once stimulus watchers and graph hooks land, update IMPLEMENTATION and HEALTH with real paths.

### Tests to Run

```bash
# Pending: integration checks once graph service wiring exists.
```

### Immediate

- [ ] Decide where Place registry lives (ngram vs graph service).

### Later

- [ ] Define EvidenceRef schema (string vs structured object).
- IDEA: Draft a minimal health runner for architecture-level checks.

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Focused; the main risk is over-specifying implementation details before code exists.

**Threads I was holding:**
Cross-repo linkage, async plan ownership, and how to validate repo/graph separation.

**Intuitions:**
Keep the plan centralized in `blood-ledger` until runtime wiring begins.

**What I wish I'd known at the start:**
The chain already existed conceptually; only the missing docs needed creation.

---

## POINTERS

| What | Where |
|------|-------|
| Raw architecture source | `data/ARCHITECTURE — Cybernetic Studio.md` |
| Async implementation plan (partial) | `/home/mind-protocol/the-blood-ledger/docs/infrastructure/async/SYNC_Async_Architecture.md` |
