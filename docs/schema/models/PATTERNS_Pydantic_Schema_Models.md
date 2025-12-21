# Schema Models — Patterns: Redirect to Canonical Data Model Patterns

```
STATUS: DESIGNING
UPDATED: 2025-12-21
```

---

## WHAT CHANGED

- Canonical `PATTERNS` content for schema models now lives under `docs/engine/models/PATTERNS_Models.md`; this file redirects maintain the schema path while preventing duplicate reasoning from drifting apart.
- Existing schema-focused references can still point here, but they should resolve to the engine module document for any authoring or review.

---

## TRANSITION NOTES

- Keep linking workflows anchored on `docs/engine/models/PATTERNS_Models.md` until the schema portion is phased out; redirecting ensures agents find the same chain that `ngram validate` expects.
- The schema models' BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, and HEALTH docs should remain under `docs/engine/models/` so only their template references continue pointing here.

## CHAIN

```
THIS:            PATTERNS_Pydantic_Schema_Models.md
PATTERNS:        ../../engine/models/PATTERNS_Models.md
BEHAVIORS:       ../../engine/models/BEHAVIORS_Models.md
ALGORITHM:       ../../engine/models/ALGORITHM_Models.md
VALIDATION:      ../../engine/models/VALIDATION_Models.md
IMPLEMENTATION:  ../../engine/models/IMPLEMENTATION_Models.md
HEALTH:          ../../engine/models/HEALTH_Models.md
SYNC:            ../../engine/models/SYNC_Models.md
```
