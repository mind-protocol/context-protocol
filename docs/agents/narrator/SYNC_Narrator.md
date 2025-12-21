# Narrator — Sync: Current State

```
STATUS: CANONICAL
UPDATED: 2025-12-20
```

## MATURITY

STATUS: CANONICAL

What's canonical (v1):
- Narrator prompt chain, SSE streaming, and CLI orchestration are stable.
- The "Two Paths" (conversational vs significant) logic is enforced in `CLAUDE.md`.

## CURRENT STATE

Narrator documentation is current after template alignment. The module remains stable with no code changes; focus is on Health/Implementation format updates.

## RECENT CHANGES

### 2025-12-20: Ngram Framework Refactor

- **What:** Refactored `IMPLEMENTATION_Narrator.md` and updated `TEST_Narrator.md` to the Health format.
- **Why:** To align with the new ngram documentation standards and emphasize DATA FLOW AND DOCKING.
- **Impact:** Narrator module documentation is now compliant; Health checks are anchored to prompt building and agent output.

### 2025-12-26: Fortified implementation template

- **What:** Added explicit RUNTIME BEHAVIOR, BIDIRECTIONAL LINKS, and GAPS sections to `IMPLEMENTATION_Narrator.md`.
- **Why:** Close the DOC_TEMPLATE_DRIFT warning so the implementation doc now matches the template and documents the runtime story.
- **Files:** `docs/agents/narrator/IMPLEMENTATION_Narrator.md`, `docs/agents/narrator/SYNC_Narrator.md`
- **Verification:** `ngram validate`

## HANDOFF: FOR AGENTS

Use VIEW_Implement_Write_Or_Modify_Code for prompt changes. Ensure any new narrator tools are reflected in `TOOL_REFERENCE.md` and the Health docks.

## TODO

- [ ] Consolidate narrator schema references under `docs/schema/SCHEMA.md`.
- [ ] Implement hallucination detection for unprompted entity creation.

## POINTERS

- `docs/agents/narrator/PATTERNS_Narrator.md` for authorial intent.
- `docs/agents/narrator/IMPLEMENTATION_Narrator.md` for CLI orchestration.
- `agents/narrator/CLAUDE.md` for the core authorial instructions.

## CHAIN

```
THIS:            SYNC_Narrator.md (you are here)
PATTERNS:        ./PATTERNS_Narrator.md
BEHAVIORS:       ./BEHAVIORS_Narrator.md
ALGORITHM:       ./ALGORITHM_Scene_Generation.md
VALIDATION:      ./VALIDATION_Narrator.md
IMPLEMENTATION:  ./IMPLEMENTATION_Narrator.md
HEALTH:          ./HEALTH_Narrator.md
```
