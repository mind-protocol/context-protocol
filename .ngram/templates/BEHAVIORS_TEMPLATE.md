# {Module Name} — Behaviors: {Brief Description of Observable Effects}

```
STATUS: DRAFT | REVIEW | STABLE
CREATED: {DATE}
VERIFIED: {DATE} against {COMMIT}
```

---

## CHAIN

```
OBJECTIFS:      ./OBJECTIFS_{name}.md
THIS:            BEHAVIORS_*.md (you are here)
PATTERNS:        ./PATTERNS_*.md
MECHANISMS:     ./MECHANISMS_*.md (if applicable)
ALGORITHM:       ./ALGORITHM_*.md
VALIDATION:      ./VALIDATION_{name}.md
HEALTH:          ./HEALTH_{name}.md
IMPLEMENTATION:  ./IMPLEMENTATION_*.md
SYNC:            ./SYNC_{name}.md

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

## OBJECTIVES SERVED

| Behavior ID | Objective | Why It Matters |
|-------------|-----------|----------------|
| B1 | {Objective} | {what the behavior protects or enables} |
| B2 | {Objective} | {what the behavior protects or enables} |

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

## MARKERS

> See VIEW_Escalation for full YAML formats. Use `ngram solve-markers` to triage.

<!-- @ngram:todo
title: "{Behavior that needs clarification}"
priority: {low|medium|high|critical}
context: |
  {Why this behavior needs attention}
task: |
  {Concrete clarification or fix needed}
-->

<!-- @ngram:proposition
title: "{Potential future behavior}"
priority: {1-10}
context: |
  {Why this behavior would be valuable}
implications: |
  {How it changes existing behavior}
suggested_changes: |
  {What behaviors to add or modify}
-->

<!-- @ngram:escalation
task_name: "{Uncertain edge case needing decision}"
priority: {1-10}
category: {behavior-needed|scope-needed|...}
context: |
  {Current behavior, unclear edge case}
questions:
  - "{What should happen in this case?}"
-->
