# Schema Models — Sync: Redirect

```
STATUS: DESIGNING
LAST_UPDATED: 2025-12-21
UPDATED_BY: codex
```

---

## WHAT CHANGED

- The canonical schema-model SYNC now lives under `docs/engine/models/SYNC_Models.md`; this file redirects schema-area references while channeling edits to the engine module.
- `PATTERNS_Pydantic_Schema_Models.md` now points at `docs/engine/models/PATTERNS_Models.md`, so all design reasoning for the Pydantic schema models is authored from one location even though schema-area links still have a landing spot.

---

## TRANSITION NOTES

- Canonical location: `docs/engine/models/SYNC_Models.md`
- Schema PATTERNS now use: `docs/engine/models/PATTERNS_Models.md` (via the redirect in `PATTERNS_Pydantic_Schema_Models.md`)
- Doc chain to follow: `docs/engine/models/PATTERNS_Models.md`, `docs/engine/models/BEHAVIORS_Models.md`, `docs/engine/models/IMPLEMENTATION_Models.md`
- Reason: DOC_DUPLICATION-models-SYNC_Schema_Models flagged the schema and engine SYNC docs as redundant, so this sheet now points to the engine module.

---

## CHAIN

```
THIS:            SYNC_Schema_Models.md
PATTERNS:        ../../engine/models/PATTERNS_Models.md
BEHAVIORS:       ../../engine/models/BEHAVIORS_Models.md
ALGORITHM:       ../../engine/models/ALGORITHM_Models.md
VALIDATION:      ../../engine/models/VALIDATION_Models.md
IMPLEMENTATION:  ../../engine/models/IMPLEMENTATION_Models.md
HEALTH:          ../../engine/models/HEALTH_Models.md
```
