# Graph Health — Patterns: Schema-Driven Validation And Query Artifacts

```
CREATED: 2025-12-19
STATUS: DESIGNING
```

---

## CHAIN

```
THIS:            PATTERNS_Graph_Health_Validation.md
SYNC:            ./SYNC_Graph_Health.md

IMPL:            engine/graph/health/check_health.py
```

---

## THE PROBLEM

The graph is the canonical story state, but drift and malformed data silently
break the narrative. Without a schema-aware health layer, invalid nodes or links
surface only when a scene fails or a query returns nonsense. The project also
needs a shared library of graph queries so narrative and debugging workflows
are repeatable instead of ad hoc.

---

## THE PATTERN

Use a YAML schema (`schema.yaml`) as the single source of truth for node/link
requirements and enum values. Build two validation paths on top of it:

- A CLI health check (`check_health.py`) that counts nodes/links, flags missing
  required fields, and reports invalid enums against a live graph.
- A test suite (`test_schema.py`) that asserts schema invariants with targeted
  queries for required fields, enums, and relationship expectations.

Pair the validation with a curated query library (`example_queries.cypher`) and
annotated outputs (`query_outputs.md`, `query_results.md`) so the team has a
shared, rated toolbox for inspection and narrative setup.

---

## PRINCIPLES

### Principle 1: Schema Is The Authority

The YAML schema is the contract. Validation tools read it directly so there is
one place to update when the graph model changes.

### Principle 2: Read-Only Health Checks

The health check is diagnostic, not corrective. It reports issues and leaves
mutation to explicit tooling or human decisions.

### Principle 3: Queries Are First-Class Artifacts

Queries live in versioned files with ratings and expected outputs so narrative
workflows and debugging stay repeatable.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| engine/db/graph_ops.py | GraphOps provides the query interface to FalkorDB. |
| falkordb | Live graph access for schema tests and terminology lints. |
| yaml | Loads schema definitions for validation. |

---

## INSPIRATIONS

- Database schema validation patterns from data pipelines that enforce
  repeatable, versioned checks against evolving data.
- Test-first data quality checks used in ETL workflows to catch bad records
  before they leak into production dashboards or reports.
- Curated query collections used in Cypher tooling that standardize how teams
  inspect graph health and share investigative recipes.

---

## SCOPE

This pattern covers schema-aligned validation and query artifacts for the
graph health tooling only. It includes the CLI check, pytest validation,
terminology linting, and curated Cypher query files, but not broader graph
engineering workflows outside the health module.

---

## WHAT THIS DOES NOT SOLVE

- Automatic fixes or migrations for invalid data; remediation remains a
  separate manual or scripted workflow outside the health checks.
- Full schema evolution tooling such as versioned diffs, migrations, or
  compatibility layers between schema revisions.
- Performance tuning for very large graphs, including index planning or query
  optimization beyond the current diagnostic focus.

---

## MARKERS

<!-- @ngram:todo Should link property validation expand beyond enum checks for required -->
  metadata and relationship-level invariants?
<!-- @ngram:todo Decide if health checks should run in CI with a seeded graph so schema -->
  drift is caught before integration tests.
<!-- @ngram:proposition Add a report export format (CSV or markdown) that includes summaries, -->
  query outputs, and timestamped audit metadata.
