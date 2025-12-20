# VIEW: Escalation & Proposition

**How to handle vague tasks, missing information, complex non-obvious problems, and agent-generated proposals.**

---

## VISION

ngram is a framework for AI-driven development, but design and implementation are an iterative discovery process with humans. Escalation exists because agents must talk to humans to converge on the right understanding. The goal is to develop great systems and products by keeping humans and agents aligned.

---

## THE PATTERN

Escalation markers prevent silent assumptions and capture uncertainty where it actually occurs. They:
- Make blockers visible and searchable
- Preserve the reasoning trail (what was checked, what is missing)
- Reduce back-and-forth by asking the right questions once
- Tell future agents exactly why a decision was needed

A good escalation makes the human response immediately actionable without re-reading the entire context.

---

## HOW ESCALATION WORKS

1. Add an `@ngram&#58;escalation` marker in the most relevant file near the issue.
2. `ngram solve-markers` picks it up.
3. The manager asks the human to resolve it.
4. The human response is added in the same location with an explicit resolution note.

---

## HOW PROPOSITION WORKS

1. An agent adds an `@ngram&#58;proposition` marker in the most relevant file near a suggested improvement.
2. `ngram solve-markers` (or `ngram doctor`) picks it up.
3. The proposition is presented for human review.
4. If approved, the human applies the suggested changes and removes the marker.

---

## HOW TODO WORKS

1. An agent or manager adds an `@ngram&#58;todo` marker in the most relevant file near the task.
2. `ngram solve-markers` (or `ngram doctor`) picks it up.
3. The manager triages the task with the human and assigns ownership.
4. The assignee completes the task and removes the marker.

---

## WHEN TO ESCALATE (PRECISE)

Escalate **only** when the next step is blocked by missing human input that cannot be inferred from:
- Docs (PATTERNS/BEHAVIORS/ALGORITHM/VALIDATION/SYNC)
- Implementation
- Repo map
- Prior decisions

**Examples (escalate):**
- Two behaviors are documented and both are implemented; choosing one changes user-visible outcomes.
- A migration could drop historical billing data; risk acceptance is required.
- A new feature changes user workflow and multiple plausible intents exist.
- A performance optimization could change correctness or determinism.
- A third-party API is ambiguous and impacts core logic.

---

## WHEN NOT TO ESCALATE

Do not escalate when:
- The decision is low impact
- The answer is already documented
- The outcome is reversible and safe

**Examples (do not escalate):**
- Renaming variables to match an existing naming convention
- Reformatting or minor refactors with no behavior change
- Adding a missing comment to align with docs
- Fixing an obvious bug with a single correct fix
- Resolving lint/format/style issues already covered by conventions
- Adding a missing test when behavior is already documented
- Updating a config key to match the existing schema without changing meaning
- Replacing a deprecated API call with its documented direct substitute
- Moving code into an already defined module to match structure

---

## ESCALATION TYPES

Use one category:
- objective-needed — goal or success criteria are missing or unclear.
- context-needed — missing constraints, background, or dependencies.
- design-choice-needed — multiple valid designs exist and a choice matters.
- tradeoff-needed — performance/complexity/maintainability tension needs a call.
- scope-needed — unclear what is in vs out of scope.
- risk-acceptance-needed — human must accept a known risk or debt.
- ambiguity-needed — requirements are vague or conflicting.
- inconsistency — docs/code disagree and a decision is required.
- confusion — intent is unclear and needs clarification.
- validation-needed — requires permission for destructive or risky action.
- data-needed — missing data/examples block the decision.
- behavior-needed — expected behavior/edge cases are undefined.
- naming-needed — terminology/vocabulary choice is required.

---

## ESCALATION MARKER FORMAT (YAML)

```
@ngram&#58;escalation

task_name: "Choose streaming vs batch ingestion to meet dashboard freshness for analytics" # one-line decision with scope + goal

priority: 8 # 1-10; 10=fully blocked, 7-9=core path blocked, 4-6=important, 1-3=nice-to-have

hooks:
  - claude_code_hook # include if the manager should surface this escalation during conversations

context: | # 1-2 paragraphs: current system, where the issue appears, and why it matters
  We are building the analytics pipeline for near-real-time dashboards used by operations and product teams.
  The pipeline currently ingests events via a nightly batch job in `src/analytics/batch_ingest.py`, which
  powers dashboards in `src/dashboard/op_metrics.py` and `src/dashboard/product_metrics.py`.

  Introducing streaming ingestion via `src/analytics/stream_ingest.py` would change infra cost, operational
  complexity, and latency expectations, and it could affect how `src/analytics/storage/event_store.py`
  models idempotency and ordering.

goal: | # observable success criteria with metric/threshold
  Ops and product dashboards update within 5 minutes of new user events (signup, purchase, refund)
  without data loss or double counting.

current_subgoal: | # the exact next action blocked right now
  Select ingestion mode before wiring schema validation in `src/analytics/validation/schema_rules.py`
  and storage adapters in `src/analytics/storage/`.

category: tradeoff-needed # pick closest escalation type (do not invent new types)

nature: question # question for a choice; problem for a contradiction

why_blocked: | # specific missing information or decision, not a generic excuse
  Both modes satisfy correctness, but the choice depends on product priorities: latency vs cost vs ops burden.
  No document or prior decision specifies the acceptable tradeoff.

evidence: # concrete sources checked already
  - "Reviewed docs/analytics/BEHAVIORS_Analytics.md and docs/analytics/SYNC_Analytics_State.md"
  - "Checked src/analytics/batch_ingest.py and src/analytics/stream_ingest.py"
  - "Reviewed cost notes in docs/infra/ALGORITHM_Infra_Cost_Model.md"

links: # only the most relevant pointers
  files:
    - path: src/analytics/stream_ingest.py # files that matter to the decision
    - path: src/analytics/batch_ingest.py
    - path: src/analytics/storage/event_store.py
    - path: src/dashboard/op_metrics.py
  docs:
    - path: docs/analytics/BEHAVIORS_Analytics.md # doc context to read
    - path: docs/analytics/SYNC_Analytics_State.md
    - path: docs/infra/ALGORITHM_Infra_Cost_Model.md
  graph:
    - "analytics_pipeline -> event_store -> dashboards" # graph context if applicable

questions: # direct questions, one decision per question
  - "Is sub-5-minute freshness a hard requirement for v1, or can we start with hourly updates?"
  - "Is higher infra cost acceptable in exchange for lower latency?"

info_required: # minimum missing inputs needed to decide
  - "Target freshness SLA for v1"
  - "Acceptable monthly infra cost range"

precisions: # edge cases or constraints that change the decision
  - "Do we need weekly backfills of historical data?"
  - "Do refunds require real-time visibility or can they lag?"

options: # real alternatives with pros/cons + hesitation
  - option: "Streaming ingestion"
    description: "Consume events continuously and write to incremental storage with idempotent keys"
    pros:
      - "Low latency (minutes)"
      - "Near-real-time dashboards"
    cons:
      - "Higher infra cost"
      - "More operational complexity"
    hesitation:
      - "No stated cost ceiling or ops budget"
  - option: "Batch ingestion"
    description: "Keep nightly batch job and optimize incremental loads for dashboards"
    pros:
      - "Lower infra cost"
      - "Simpler operations"
    cons:
      - "Higher latency (hours)"
      - "Potential mismatch with near-real-time expectations"
    hesitation:
      - "May violate stakeholder assumptions about freshness"

waiting_decision: # explicit interim action while waiting
  choice: "implement-workaround" # implement-most-likely | implement-partial-or-degraded | implement-workaround | make-first-version | postpone
  note: "Proceed with batch ingestion but label dashboard freshness as unvalidated pending decision"

response: # optional human response fields (fill after decision)
  choice: "Streaming ingestion" # chosen option or decision summary
  task_description: "Implement streaming ingestion for v1 dashboards" # optional task statement
  pattern: "Event-driven ingestion" # optional pattern name
  behavior: "Dashboards update within 5 minutes; batch job removed" # optional behavior summary
  notes: "Approved higher infra cost for lower latency" # optional extra context
```

---

## PROPOSITION MARKER FORMAT (YAML)

```
@ngram&#58;proposition

title: "Refactor `utils.py` into smaller, cohesive modules" # Concise title for the proposition

priority: 3 # 1-10; 10=high impact, 1-3=low impact/cleanup

context: | # 1-2 paragraphs: current situation, why the proposition is beneficial
  The `utils.py` file has grown significantly and now contains a mix of unrelated
  helper functions for various parts of the application. This makes it hard to
  navigate, test, and understand dependencies.

  Splitting it into more focused modules (e.g., `file_utils.py`, `string_utils.py`)
  would improve modularity and maintainability.

implications: | # Potential impacts on existing code or system
  - Requires updating import paths in various files.
  - Improves code organization and reduces cognitive load.
  - May slightly increase the number of files in the project.

suggested_changes: | # High-level description of proposed changes
  - Create `ngram/utils/file_utils.py` and move file-related functions.
  - Create `ngram/utils/string_utils.py` and move string manipulation functions.
  - Update all call sites to import from the new modules.
  - Consider creating `ngram/utils/validation_utils.py` for validation helpers.

links: # only the most relevant pointers
  files:
    - path: ngram/utils.py # The file(s) the proposition applies to
  docs:
    - path: docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md # Related documentation
```

---

## PRIORITY SCALE (HOW TO SET)

- 10: fully blocked, no safe progress without decision
- 7-9: blocks core path or major milestone
- 4-6: important but can proceed with a workaround
- 1-3: nice-to-have or cleanup-level decisions

---

## HOOKS (WHEN TO INCLUDE)

- `claude_code_hook`: include when the manager should actively surface this escalation during conversation loops.

---

## TODO MARKER FORMAT (YAML)

```
@ngram&#58;todo
title: "Add snapshot tests for settings panel"
created_by: "agent" # agent | manager | human
priority: medium # low | medium | high | critical
context: |
  1-2 paragraphs explaining why this task exists and what it unblocks.
task: |
  The concrete work to perform, including any key constraints.
paths:
  - path: src/settings/ # optional paths to touch
```
