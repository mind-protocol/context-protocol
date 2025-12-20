# {Module Name} — Validation: {Brief Description of Invariants and Tests}

```
STATUS: DRAFT | REVIEW | STABLE
CREATED: {DATE}
VERIFIED: {DATE} against {COMMIT}
```

---

## CHAIN

```
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

## GAPS / IDEAS / QUESTIONS

- [ ] {Missing test}
- [ ] {Invariant that needs formal verification}
- IDEA: {Additional property to test}
- QUESTION: {Unclear validation requirement}
