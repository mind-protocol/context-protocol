# {Module Name} — Behaviors: {Brief Description of Observable Effects}

```
STATUS: DRAFT | REVIEW | STABLE
CREATED: {DATE}
VERIFIED: {DATE} against {COMMIT}
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_*.md
THIS:            BEHAVIORS_*.md (you are here)
ALGORITHM:       ./ALGORITHM_*.md
VALIDATION:      ./VALIDATION_*.md
IMPLEMENTATION:  ./IMPLEMENTATION_*.md
TEST:            ./TEST_*.md
SYNC:            ./SYNC_*.md

IMPL:            {path/to/main/source/file.py}
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: {Behavior Name}

```
GIVEN:  {precondition — what state must exist}
WHEN:   {action or trigger — what happens}
THEN:   {outcome — what should result}
AND:    {additional outcome if needed}
```

### B2: {Behavior Name}

```
GIVEN:  {precondition}
WHEN:   {action}
THEN:   {outcome}
```

### B3: {Behavior Name}

```
GIVEN:  {precondition}
WHEN:   {action}
THEN:   {outcome}
```

---

## INPUTS / OUTPUTS

### Primary Function: `{function_name}()`

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| {name} | {type} | {what it is} |
| {name} | {type} | {what it is} |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| {name} | {type} | {what it is} |

**Side Effects:**

- {What state changes, if any}
- {What external effects, if any}

---

## EDGE CASES

### E1: {Edge Case Name}

```
GIVEN:  {unusual or boundary condition}
THEN:   {what should happen}
```

### E2: {Edge Case Name}

```
GIVEN:  {unusual condition}
THEN:   {what should happen}
```

---

## ANTI-BEHAVIORS

What should NOT happen:

### A1: {Anti-Behavior Name}

```
GIVEN:   {condition}
WHEN:    {action}
MUST NOT: {what should never happen}
INSTEAD:  {what should happen}
```

### A2: {Anti-Behavior Name}

```
GIVEN:   {condition}
WHEN:    {action}
MUST NOT: {bad outcome}
INSTEAD:  {correct outcome}
```

---

## GAPS / IDEAS / QUESTIONS

- [ ] {Open question}
- [ ] {Behavior that needs clarification}
- IDEA: {Potential future behavior}
- QUESTION: {Uncertain edge case}
