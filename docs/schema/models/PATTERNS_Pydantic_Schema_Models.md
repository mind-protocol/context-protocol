# Schema Models — Patterns: Pydantic Graph Schema Models

```
STATUS: DESIGNING
CREATED: 2025-12-19
```

---

## CHAIN

```
THIS:  PATTERNS_Pydantic_Schema_Models.md
SYNC:  ../../engine/models/SYNC_Models.md
IMPL:  engine/models/__init__.py
```

---

## THE PROBLEM

The engine needs a single, validated schema for nodes, links, tensions, and
moments so all subsystems speak the same language. Without a canonical set of
models, serialization, validation, and LLM-facing contracts drift and gameplay
state becomes inconsistent.

---

## THE PATTERN

Define the schema as Pydantic models and enums, split by responsibility:
base enums and shared structures in `base.py`, node models in `nodes.py`, link
models in `links.py`, and tension models in `tensions.py`. Keep the module
re-export layer in `__init__.py` so other systems import one stable surface.

---

## PRINCIPLES

### Principle 1: Schema As Contract

All gameplay data structures are expressed as Pydantic models, giving a single
source of truth for validation and serialization.

### Principle 2: Separate Enums From Entities

Enums and shared shapes live in `base.py`, allowing node/link models to remain
focused on domain fields rather than taxonomy definitions.

### Principle 3: Computed Helpers Stay Close

Lightweight helpers (like embeddable text or link intensity) live on the model
they describe so downstream systems can rely on consistent behavior.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `pydantic` | Validation, defaults, and serialization for schema models |
| `docs/schema/SCHEMA.md` | Canonical schema definitions and version context |

---

## INSPIRATIONS

- Pydantic's validation and JSON schema export patterns, which keep the schema
  contract explicit and make model intent legible across services, aligning
  with how schema expectations surface in tests and tooling.
- The shared schema glossary in `docs/schema/SCHEMA.md`, anchoring consistent
  field naming and enum meanings across engine subsystems and graph health
  checks.

---

## SCOPE

### In Scope

- Pydantic classes, enums, and shared base shapes for nodes, links, and
  tensions that define canonical schema surfaces for the engine, including
  shared identifiers and timestamp shapes.
- Field defaults, optionality, and helper properties that remain data-adjacent
  so model behavior stays predictable and portable.

### Out of Scope

- Graph storage, query APIs, and persistence behavior, which live in graph and
  physics layers rather than the schema-model definitions or migrations.
- Runtime rule enforcement (physics ticks, tension flips, narrative gating)
  that belongs to system logic outside the schema layer.

---

## WHAT THIS DOES NOT SOLVE

- Graph persistence or query logic, which live in graph/physics layers and storage.
- Relationship integrity across nodes/links beyond field validation checks.
- Runtime enforcement of world rules, which is owned by physics and runtime services.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Document validation invariants specific to model interactions.
- [ ] Decide whether a dedicated schema validation test suite is needed beyond `engine/tests/test_models.py`.
