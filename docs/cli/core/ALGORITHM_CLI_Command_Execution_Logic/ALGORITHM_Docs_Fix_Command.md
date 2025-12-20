# ngram Framework CLI — Algorithm: Docs Fix Command

```
STATUS: DESIGNING
CREATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ../PATTERNS_Why_CLI_Over_Copy.md
BEHAVIORS:       ../BEHAVIORS_CLI_Command_Effects.md
THIS:            ALGORITHM_Docs_Fix_Command.md
VALIDATION:      ../VALIDATION_CLI_Instruction_Invariants.md
IMPLEMENTATION:  ../IMPLEMENTATION_CLI_Code_Architecture/IMPLEMENTATION_Overview.md
HEALTH:          ../HEALTH_CLI_Command_Test_Coverage.md
SYNC:            ../SYNC_CLI_Development_State.md

IMPL:            ngram/docs_fix.py
```

---

## OVERVIEW

The `ngram docs-fix` command repairs documentation chains and adds missing
minimum docs to keep protocol invariants satisfied without manual edits.

---

## ALGORITHM: `docs_fix_command()`

1. Create minimal missing docs for CLI and schema modules.
2. Ensure world-runner health doc exists.
3. Fix broken CHAIN links by rewriting paths to existing targets.
4. Report a summary of changes.
