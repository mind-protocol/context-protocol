# Skill: `ngram.solve_markers`
@ngram:id: SKILL.MARKERS.TRIAGE

## Maps to VIEW
`VIEW_Escalation_How_To_Handle_Vague_Tasks_Missing_Information_And_Complex_Non-Obvious_Problems.md`

## Purpose
Find, triage, and resolve @ngram markers across the codebase. This skill handles three marker types:
- **Escalations**: Blockers requiring human decisions
- **Propositions**: Agent suggestions for improvements
- **Todos**: Actionable tasks needing assignment and completion

## CLI Command
```bash
ngram solve-markers
```

## Inputs (from marker scan)
```yaml
markers_found:
  escalations:
    - file: "<path>"
      priority: <1-10>
      category: "<type>"
      context: "<summary>"
  propositions:
    - file: "<path>"
      priority: <1-10>
      title: "<improvement>"
  todos:
    - file: "<path>"
      priority: "<low|medium|high|critical>"
      title: "<task>"
```

## Outputs (YAML)
```yaml
resolved:
  - file: "<path>"
    marker_type: "<escalation|proposition|todo>"
    resolution: "<decision|approved|completed|rejected>"
    notes: "<context>"
pending:
  - file: "<path>"
    reason: "<why unresolved>"
```

## Marker Formats

### @ngram:escalation
```yaml
@ngram:escalation
task_name: "<Decision needed with scope + goal>"
priority: <1-10>  # 10=fully blocked, 7-9=core path, 4-6=important, 1-3=nice-to-have
category: "<type>"  # objective-needed, context-needed, design-choice-needed, etc.
context: |
  <Current system, where issue appears, why it matters>
goal: |
  <Observable success criteria>
questions:
  - "<Direct question requiring decision>"
options:
  - option: "<choice>"
    pros: ["<benefit>"]
    cons: ["<cost>"]
response:  # Fill after human decision
  choice: "<decision>"
  notes: "<rationale>"
```

### @ngram:proposition
```yaml
@ngram:proposition
title: "<Improvement idea>"
priority: <1-10>
context: |
  <Current situation, why beneficial>
implications: |
  <Impacts on existing code>
suggested_changes: |
  <High-level proposed modifications>
```

### @ngram:todo
```yaml
@ngram:todo
title: "<Actionable task>"
created_by: "<agent|manager|human>"
priority: "<low|medium|high|critical>"
context: |
  <Why this task exists and what it unblocks>
task: |
  <Concrete work to perform>
paths:
  - path: "<files to touch>"
```

## Escalation Categories
- objective-needed — goal or success criteria missing
- context-needed — missing constraints/dependencies
- design-choice-needed — multiple valid designs
- tradeoff-needed — performance/complexity tension
- scope-needed — unclear in/out of scope
- risk-acceptance-needed — human must accept risk
- ambiguity-needed — requirements vague/conflicting
- inconsistency — docs/code disagree
- confusion — intent unclear
- validation-needed — permission for risky action
- data-needed — missing data blocks decision
- behavior-needed — expected behavior undefined
- naming-needed — terminology choice required

## Gates (non-negotiable)
- Escalations MUST have human response before removal
- Propositions MUST be explicitly approved or rejected
- Todos MUST be completed with evidence before removal
- Never delete markers without resolution

## Priority Scale
- 10: Fully blocked, no safe progress
- 7-9: Blocks core path or major milestone
- 4-6: Important but can proceed with workaround
- 1-3: Nice-to-have or cleanup-level

## Doctor Integration
`ngram doctor` automatically detects:
- ESCALATION markers (severity: warning)
- PROPOSITION markers (severity: info)
- TODO markers (severity: info)

Run `ngram solve-markers` to triage all markers in priority order.

## Workflow
1. Run `ngram solve-markers` to list all markers
2. Review in priority order (escalations first)
3. For escalations: provide decision in `response` field
4. For propositions: approve (implement) or reject (delete)
5. For todos: assign, complete task, then delete marker
6. Update SYNC files with resolution notes

## Evidence & Referencing
- Docs: `@ngram:id + file + header path`
- Code: `file:line + symbol`
- Graph: `node_id -> relationship -> node_id`

## Never-Stop Rule
If blocked on a marker, log the blocker and switch to next unblocked task.
