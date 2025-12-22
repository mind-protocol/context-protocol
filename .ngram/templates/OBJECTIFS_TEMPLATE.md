# OBJECTIFS — {Module}

```
STATUS: DRAFT | REVIEW | STABLE
CREATED: {DATE}
VERIFIED: {DATE} against {COMMIT}
```

## PRIMARY OBJECTIVES (ranked)
1. {Objective} — {why it matters}
2. {Objective} — {why it matters}
3. {Objective} — {why it matters}

## NON-OBJECTIVES
- {What we explicitly do NOT optimize}
- {What this module will not attempt}

## TRADEOFFS (canonical decisions)
- When {X} conflicts with {Y}, choose {X}.
- We accept {cost} to preserve {value}.

## SUCCESS SIGNALS (observable)
- {metric/behavior}
- {metric/behavior}

---

## MARKERS

> See VIEW_Escalation for full YAML formats. Use `ngram solve-markers` to triage.

<!-- @ngram:todo
title: "{Objective refinement needed}"
priority: {low|medium|high|critical}
context: |
  {Why this objective needs clarification}
task: |
  {Specific refinement or decision to make}
-->

<!-- @ngram:proposition
title: "{New objective or priority change}"
priority: {1-10}
context: |
  {Why this would improve the module}
implications: |
  {How it changes tradeoffs}
suggested_changes: |
  {Objectives to add or reorder}
-->

<!-- @ngram:escalation
task_name: "{Objective conflict needing resolution}"
priority: {1-10}
category: {objective-needed|scope-needed|...}
context: |
  {Current objectives, conflict observed}
questions:
  - "{Which objective takes priority?}"
-->
