# Data Models — Implementation: Pydantic Code Architecture

```
STATUS: DRAFT
CREATED: 2025-12-20
UPDATED: 2025-12-20
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Models.md
BEHAVIORS:       ./BEHAVIORS_Models.md
ALGORITHM:       ./ALGORITHM_Models.md
VALIDATION:      ./VALIDATION_Models.md
THIS:            IMPLEMENTATION_Models.md
HEALTH:          ./HEALTH_Models.md
SYNC:            ./SYNC_Models.md

IMPL:            engine/models/
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## CODE STRUCTURE

```
engine/models/__init__.py  # Module exports and high-level docs
engine/models/base.py      # Enums, shared sub-models (e.g., Skills, Atmosphere)
engine/models/nodes.py     # Character, Place, Thing, Narrative, Moment models
engine/models/links.py     # CharacterNarrative, PlacePlace, etc. models
tensions (pending import)  # Tension model
```

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `engine/models/__init__.py` | Module aggregation | Exports all models | ~90 | OK |
| `engine/models/base.py` | Core enums & shared types | `CharacterType`, `Modifier`, `GameTimestamp` | ~300 | OK |
| `engine/models/nodes.py` | Graph node definitions | `Character`, `Place`, `Thing`, `Narrative`, `Moment` | ~300 | OK |
| `engine/models/links.py` | Graph link definitions | `CharacterNarrative`, `PlacePlace` | ~200 | OK |
| `tensions` | Tension definition | `Tension` | ~100 | OK |

**Size Thresholds:**
- **OK** (<400 lines): Healthy size, easy to understand
- **WATCH** (400-700 lines): Getting large, consider extraction opportunities
- **SPLIT** (>700 lines): Too large, must split before adding more code

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Domain Model / Anemic Domain Model (with rich properties).

**Why this pattern:** The models primarily focus on data structure and validation (anemic), but also include rich `@property` methods (e.g., `has_flipped` in `Tension`) and `embeddable_text` functions that provide some behavior. This balances strict data representation with domain-specific utility.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Pydantic `BaseModel` | All models | Schema definition, validation, serialization |
| Python `enum Enum` | All `*Type` fields | Type-safe enumeration of valid choices |
| `@property` decorator | `Tension has_flipped`, `CharacterPlace is_present` | Derived attributes for clear state querying |
| `default_factory` | `List` fields, nested models | Ensure mutable defaults are independent per instance |

### Anti-Patterns to Avoid

- **Logic Sprawl**: Avoid adding complex business logic directly into models; defer to services (e.g., `GraphOps`, `Orchestrator`).
- **Redundant Validation**: Do not re-implement Pydantic's native validation checks with custom `@validator` functions unless truly necessary.
- **Circular Dependencies**: Structure files to avoid `A imports B` and `B imports A` loops, especially between `engine/models/nodes.py`, `engine/models/links.py`, `engine/models/base.py`.

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Data Models | Schema definition, basic validation, derived properties | Graph operations, API endpoints, game logic | Pydantic instances (dict, JSON) |

---

## SCHEMA

The primary schema is the sum of all Pydantic models in this module. Refer to individual model definitions in `engine/models/nodes.py`, `engine/models/links.py`, `tensions`, and `engine/models/base.py` for full details. High-level schema contracts for specific domains (e.g., Moment Graph) are documented in `docs/schema/`.

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| Model instantiation | `engine/models/nodes.py:Character(...)` | World scraping, API, Orchestrator |
| `GameTimestamp.parse()` | `engine/models/base.py:284` | Parsing game event strings |
| `embeddable_text()` | `engine/models/nodes.py:100` | `EmbeddingService` for vectorization |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### Data Ingestion: Raw Input → Validated Model

This flow describes how raw data (from files, API, etc.) is transformed into validated Python objects.

```yaml
flow:
  name: model_ingestion
  purpose: Ensure all data conforms to the defined schema and types.
  scope: Raw Data -> Pydantic Validation -> Model Instance
  steps:
    - id: step_1_load_raw
      description: Receive raw data (dict, JSON, ORM object).
      file: N/A
      function: N/A
      input: raw_data
      output: dict/object
      trigger: API call, file read, ORM query
      side_effects: none
    - id: step_2_instantiate_model
      description: Pass raw data to Pydantic model constructor.
      file: engine/models/nodes.py (e.g., Character)
      function: __init__ / parse_obj
      input: raw_data
      output: Pydantic model instance
      trigger: code calling model constructor
      side_effects: `ValidationError` on failure
  docking_points:
    guidance:
      include_when: data enters or leaves the system
    available:
      - id: raw_data_input
        type: custom
        direction: input
        file: engine/models/nodes.py (e.g., Character)
        function: __init__
        trigger: various (API, scraper)
        payload: dict
        async_hook: optional
        needs: none
        notes: Entry point for unstructured data
      - id: validated_model_output
        type: custom
        direction: output
        file: engine/models/nodes.py (e.g., Character)
        function: __init__
        trigger: successful instantiation
        payload: Pydantic model instance
        async_hook: not_applicable
        needs: none
        notes: Guaranteed schema compliance
    health_recommended:
      - dock_id: validated_model_output
        reason: Critical for ensuring downstream systems receive valid data.
```

---

## LOGIC CHAINS

### LC1: `GameTimestamp` Comparison

**Purpose:** Allow chronological ordering and comparison of game timestamps.

```
GameTimestamp instance (`ts1`)
  → `ts1 < ts2` (or `<=`, `>`, `>=`)
    → engine/models/base.py:GameTimestamp.__lt__ (or __le__, __gt__, __ge__)
      → Compares `day`, then `TimeOfDay` enum order
        → Boolean result
```

**Data transformation:**
- Input: Two `GameTimestamp` instances.
- Output: Boolean indicating the chronological relationship.

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
engine/models/__init__.py
    ├── imports → .base
    ├── imports → .nodes
    ├── imports → .links
    └── imports → .tensions

engine/models/nodes.py
    └── imports → .base (for enums and sub-models)

engine/models/links.py
    └── imports → .base (for enums)

engine/models/tensions
    └── imports → .base (for enums and sub-models)
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `pydantic` | Core data modeling | All files in `engine/models/` |
| `enum` | Enumerated types | `engine/models/base.py` |
| `datetime` | Date/time fields | `engine/models/base.py` |
| `typing` | Type hints | All files in `engine/models/` |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Model Data | Pydantic model instance | Per-instance | Matches object lifecycle |

### State Transitions

- Models are generally immutable once instantiated (Pydantic's default behavior).
- Updates typically involve creating a new model instance with modified data.

---

## RUNTIME BEHAVIOR

### Model Instantiation

When data is loaded from various sources (e.g., API requests, database queries, YAML files), it is passed to the Pydantic model constructors. This process immediately triggers validation and type coercion. Invalid data will raise a `ValidationError` early in the data pipeline, preventing corrupted state from propagating.

### Property Access

Derived properties (e.g., `Tension has_flipped`) are computed dynamically upon access. These computations are typically lightweight and do not involve side effects, ensuring efficient querying of model state.

### Serialization

Models are frequently serialized to dictionaries or JSON (e.g., for API responses, database storage). This process respects `Field` configurations (like `exclude=True`) to ensure only relevant data is exposed.

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| Model Validation | Synchronous | Pydantic validation is typically blocking |

**Considerations:**
- `default_factory` for mutable defaults ensures thread-safe independent instances.
- No shared mutable state within the module itself, minimizing concurrency risks at the model layer.

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `Config allow_population_by_field_name` | `Moment` model in `engine/models/nodes.py` | `True` | Allows `tick` to be set via `tick_created` alias. |
| `Field(ge=..., le=...)` | Various fields | N/A | Numeric range constraints. |
| `Field(default_factory=list)` | `List` fields | `[]` | Ensures unique mutable defaults. |

---

## BIDIRECTIONAL LINKS

### Code → Docs

| File | Line | Reference |
|------|------|-----------|
| `engine/models/__init__.py` | 5 | `docs/schema/models/PATTERNS_Pydantic_Schema_Models.md` |
| `engine/models/base.py` | 5 | `docs/engine/models/VALIDATION_Models.md` |
| `engine/models/nodes.py` | 5 | `docs/engine/models/PATTERNS_Models.md` |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| Character model | `engine/models/nodes.py:Character` |
| Place model | `engine/models/nodes.py:Place` |
| Tension model | `engine/models/tensions:Tension` |
| `GameTimestamp` operations | `engine/models/base.py:GameTimestamp` |

---

## MARKERS

### Missing Implementation

<!-- @ngram:todo Custom validation for mutually exclusive fields (e.g., `Narrative source` vs. `Narrative detail`). -->
<!-- @ngram:todo More robust `__eq__` and `__hash__` methods for all models to enable reliable set/dict usage. -->

### Ideas

<!-- @ngram:proposition Generate JSON Schema for all models and use it for API documentation and frontend validation. -->
<!-- @ngram:proposition Implement `Config.extra = 'forbid'` to prevent accidental inclusion of unknown fields. -->

### Questions

<!-- @ngram:escalation How can we best manage schema evolution without breaking existing saved graph data? -->
<!-- @ngram:escalation Should `Moment`'s `tick` property (alias for `tick_created`) be removed for clarity in new code? -->
