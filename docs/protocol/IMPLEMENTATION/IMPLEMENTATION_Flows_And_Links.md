# ngram Framework — Implementation: Flows and Links

```
STATUS: STABLE
CREATED: 2025-12-18
```

---

## CHAIN

```
PATTERNS:        ../PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md
BEHAVIORS:       ../BEHAVIORS_Observable_Protocol_Effects.md
ALGORITHM:       ../ALGORITHM_Overview.md
VALIDATION:      ../VALIDATION_Protocol_Invariants.md
IMPLEMENTATION:  ../IMPLEMENTATION_Overview.md
THIS:            ./IMPLEMENTATION_Flows_And_Links.md
TEST:            ../TEST_Protocol_Test_Cases.md
SYNC:            ../SYNC_Protocol_Current_State.md
```

---

## ENTRY POINTS

| Entry Point | File | Triggered By |
|-------------|------|--------------|
| Bootstrap | .ngram/CLAUDE.md + AGENTS.md | Agent session start |
| Navigation | .ngram/PROTOCOL.md | After bootstrap |
| Task selection | .ngram/views/VIEW_*.md | Based on task type |
| State check | .ngram/state/SYNC_Project_State.md | Before any work |
| Module context | docs/{area}/{module}/PATTERNS_*.md | When modifying code |

---

## AGENT SESSION FLOW

```
Agent starts
  → read .ngram/CLAUDE.md / AGENTS.md
  → read PROTOCOL + PRINCIPLES
  → load SYNC_Project_State
  → select VIEW_{Task}
  → load module docs
  → do work
  → update SYNC files
```

---

## DOCUMENTATION CHAIN FLOW

```
PATTERNS → BEHAVIORS → ALGORITHM → VALIDATION → IMPLEMENTATION → TEST → SYNC
```

---

## BIDIRECTIONAL LINKS

### Code → Docs

```python
# DOCS: docs/{area}/{module}/PATTERNS_*.md
```

### Docs → Code

| Doc Section | Points To |
|-------------|-----------|
| PATTERNS: Dependencies | Module imports |
| IMPLEMENTATION: Code structure | File paths |
| VALIDATION: Invariants | Test files |
| SYNC: Pointers | Key file locations |

---

## DEPENDENCIES (INTERNAL)

```
.ngram/CLAUDE.md
  → PROTOCOL.md
  → PRINCIPLES.md
PROTOCOL.md
  → views/VIEW_*.md
  → templates/*_TEMPLATE.md
VIEW_*.md
  → state/SYNC_Project_State.md
  → docs/{area}/{module}/*.md
modules.yaml
  → code paths
  → docs paths
```
