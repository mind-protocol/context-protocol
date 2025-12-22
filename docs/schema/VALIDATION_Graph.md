# Graph Validation

This schema-level validation page is a redirect to the canonical living-graph
validation spec. It exists so schema chain references remain stable while
the authoritative validation rules live with the physics graph module.

---

## CHAIN

```
PATTERNS:   ../physics/graph/PATTERNS_Graph.md
BEHAVIORS:  ../physics/graph/BEHAVIORS_Graph.md
ALGORITHM:  ../physics/ALGORITHM_Physics.md
VALIDATION: ../physics/graph/VALIDATION_Living_Graph.md
THIS:       VALIDATION_Graph.md
```

---

## INVARIANTS

The schema graph must never allow orphaned nodes, missing link targets, or
type/field mismatches against the schema definitions. Integrity checks must
preserve valid mutations while rejecting invalid entries with traceable
errors, matching the invariants spelled out in the canonical validation doc.

---

## PROPERTIES

Validation should be deterministic for the same mutation batch and schema
state, producing identical error classifications and persistence results.
Schema-level checks are expected to be idempotent and consistent across
health checks, manual runs, and automated test execution.

---

## ERROR CONDITIONS

Errors include missing required fields, invalid enum values, links that
reference absent nodes, disconnected clusters, and database unavailability.
These conditions must be surfaced as actionable errors and never silently
persisted, per the canonical validation specification.

---

## TEST COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| Invariants: orphan-free graph | `engine/graph/health/test_schema.py` | ✓ covered |
| Properties: deterministic results | `engine/tests/test_spec_consistency.py` | ✓ covered |
| Errors: invalid schema fields | `engine/graph/health/test_schema.py` | ✓ covered |
| Errors: missing targets | `engine/graph/health/test_schema.py` | ✓ covered |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] Run schema health checks to confirm invariants are enforced
[ ] Validate a mutation batch and confirm partial persistence works
[ ] Compare results against docs/physics/graph/VALIDATION_Living_Graph.md
[ ] Record any drift in docs/physics/graph/SYNC_Graph.md
```

### Automated

```bash
python -m pytest engine/graph/health/test_schema.py
python -m pytest engine/tests/test_spec_consistency.py
```

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-19
VERIFIED_AGAINST:
    canonical: docs/physics/graph/VALIDATION_Living_Graph.md
VERIFIED_BY: documentation alignment review
RESULT:
    invariants: NOT RUN
    properties: NOT RUN
    error_conditions: NOT RUN
```

---

## MARKERS

<!-- @ngram:todo Confirm the graph-health tests cover disconnected cluster detection for -->
  new node batches, and add a targeted test if coverage is incomplete.
<!-- @ngram:proposition Add a lightweight schema smoke test that runs on CI without FalkorDB, -->
  exercising enum/required-field validation in isolation.
<!-- @ngram:escalation Should schema validation explicitly report cycle checks for link -->
  types like supersedes, or should those remain in physics-layer validation?
