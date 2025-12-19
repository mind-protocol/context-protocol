# ngram Framework — Algorithm: Module Workflows

```
STATUS: STABLE
CREATED: 2024-12-15
```

---

## CHAIN

```
PATTERNS:        ../PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md
BEHAVIORS:       ../BEHAVIORS_Observable_Protocol_Effects.md
ALGORITHM:       ../ALGORITHM_Overview.md
THIS:            ./ALGORITHM_Module_Workflows.md
VALIDATION:      ../VALIDATION_Protocol_Invariants.md
IMPLEMENTATION:  ../IMPLEMENTATION_Overview.md
TEST:            ../TEST_Protocol_Test_Cases.md
SYNC:            ../SYNC_Protocol_Current_State.md
```

---

## ALGORITHM: Create New Module

1. Create `docs/{area}/{module}/`.
2. Write PATTERNS first (copy from template).
3. Write SYNC (copy from template).
4. Implement code and add DOCS reference to the header.
5. Add BEHAVIORS/ALGORITHM/VALIDATION/TEST as needed.
6. Update project SYNC.

---

## ALGORITHM: Modify Existing Module

1. Read PATTERNS and SYNC for the module.
2. Verify change fits the design (or update PATTERNS with justification).
3. Implement the change.
4. Update BEHAVIORS/ALGORITHM/VALIDATION if applicable.
5. Always update module SYNC and project SYNC.

---

## ALGORITHM: Document Cross-Cutting Concept

1. Create `docs/concepts/{concept}/`.
2. Write CONCEPT and TOUCHES using templates.
3. Reference the concept in each module that uses it.
