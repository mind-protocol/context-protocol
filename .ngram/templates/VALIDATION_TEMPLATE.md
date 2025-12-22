# {Module Name} — Validation: {Brief Description of Invariants and Tests}

```
STATUS: DRAFT | REVIEW | STABLE
CREATED: {DATE}
VERIFIED: {DATE} against {COMMIT}
```

---

## CHAIN

```
OBJECTIFS:      ./OBJECTIFS_{name}.md
PATTERNS:        ./PATTERNS_*.md
BEHAVIORS:       ./BEHAVIORS_*.md
ALGORITHM:       ./ALGORITHM_*.md
THIS:            VALIDATION_*.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_{name}.md
HEALTH:          ./HEALTH_{name}.md
SYNC:            ./SYNC_{name}.md

IMPL:            {path/to/main/source/file.py}
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS GUARANTEED

List the BEHAVIORS this validation is necessary for and guarantees.

| Behavior ID | Behavior | Why This Validation Matters |
|-------------|----------|-----------------------------|
| B1 | {Behavior Name} | {what this validation protects} |
| B2 | {Behavior Name} | {what this validation protects} |

---

## OBJECTIVES COVERED

| Objective | Validations | Rationale |
|-----------|-------------|-----------|
| {Objective} | V1, V2 | {why these invariants protect the objective} |

---

## INVARIANTS

These must ALWAYS be true:

### V1: {Invariant Name}

```
{Formal or semi-formal statement of what must hold}
```

**Checked by:** {how to verify — test name or manual procedure}

### V2: {Invariant Name}

```
{What must hold}
```

**Checked by:** {verification method}

### V3: {Invariant Name}

```
{What must hold}
```

**Checked by:** {verification method}

---

## PROPERTIES

For property-based testing:

### P1: {Property Name}

```
FORALL {variables}:
    {property that should hold}
```

**Verified by:** `health_check_{name}` | NOT YET VERIFIED — {reason}

### P2: {Property Name}

```
FORALL {variables}:
    {property}
```

**Verified by:** `health_check_{name}` | NOT YET VERIFIED — {reason}

---

## ERROR CONDITIONS

### E1: {Error Condition}

```
WHEN:    {condition that triggers error}
THEN:    {expected error behavior}
SYMPTOM: {how this manifests}
```

**Verified by:** `health_check_{name}` | NOT YET VERIFIED — {reason}

### E2: {Error Condition}

```
WHEN:    {condition}
THEN:    {error behavior}
SYMPTOM: {manifestation}
```

**Verified by:** `health_check_{name}` | NOT YET VERIFIED — {reason}

---

## HEALTH COVERAGE

| Invariant | Signal | Status |
|-----------|--------|--------|
| V1: {name} | {indicator} | ✓ VERIFIED |
| V2: {name} | {indicator} | ⚠ NOT YET VERIFIED |
| V3: {name} | — | ⚠ NOT YET VERIFIED |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] V1 holds — {how to check}
[ ] V2 holds — {how to check}
[ ] V3 holds — {how to check}
[ ] All behaviors from BEHAVIORS_*.md work
[ ] All edge cases handled
[ ] All anti-behaviors prevented
```

### Automated

```bash
# Run tests
pytest tests/{area}/test_{module}.py

# Run with coverage
pytest tests/{area}/test_{module}.py --cov={area}/{module}
```

---

## SYNC STATUS

```
LAST_VERIFIED: {DATE}
VERIFIED_AGAINST:
    impl: {area}/{module}.py @ {COMMIT}
    test: tests/{area}/test_{module}.py @ {COMMIT}
VERIFIED_BY: {NAME or SCRIPT}
RESULT:
    V1: PASS | FAIL
    V2: PASS | FAIL
    V3: PASS | FAIL | NOT RUN
```

---

## MARKERS

> See VIEW_Escalation for full YAML formats. Use `ngram solve-markers` to triage.

<!-- @ngram:todo
title: "{Missing test or invariant needing verification}"
priority: {low|medium|high|critical}
context: |
  {Why this verification is needed}
task: |
  {Specific test or check to add}
-->

<!-- @ngram:proposition
title: "{Additional property to test}"
priority: {1-10}
context: |
  {Why this property matters}
implications: |
  {Coverage improvement}
suggested_changes: |
  {What tests or invariants to add}
-->

<!-- @ngram:escalation
task_name: "{Unclear validation requirement needing clarification}"
priority: {1-10}
category: {validation-needed|scope-needed|...}
context: |
  {Current validation state, ambiguity}
questions:
  - "{What exactly needs to be validated?}"
-->
