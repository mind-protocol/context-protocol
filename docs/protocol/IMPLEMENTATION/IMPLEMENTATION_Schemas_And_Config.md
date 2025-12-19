# ngram Framework — Implementation: Schemas and Config

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
THIS:            ./IMPLEMENTATION_Schemas_And_Config.md
TEST:            ../TEST_Protocol_Test_Cases.md
SYNC:            ../SYNC_Protocol_Current_State.md
```

---

## MODULES.YAML SCHEMA

```yaml
modules:
  {module_name}:
    code: str           # Glob pattern for source files
    docs: str           # Path to documentation directory
    tests: str          # Optional test path
    maturity: enum      # DESIGNING | CANONICAL | PROPOSED | DEPRECATED
    owner: str          # agent | human | team-name
    entry_points: list  # Main files to start reading
    internal: list      # Implementation details, not public API
    depends_on: list    # Other modules this requires
    patterns: list      # Design patterns used
    notes: str          # Quick context
```

---

## SYNC FILE STRUCTURE

```yaml
SYNC:
  required:
    - LAST_UPDATED: date
    - STATUS: enum          # CANONICAL | DESIGNING | PROPOSED | DEPRECATED
  sections:
    - MATURITY
    - CURRENT STATE
    - HANDOFF: FOR AGENTS
    - HANDOFF: FOR HUMAN
  optional:
    - CONSCIOUSNESS TRACE
    - STRUCTURE
    - POINTERS
```

---

## VIEW FILE STRUCTURE

```yaml
VIEW:
  required:
    - WHY THIS VIEW EXISTS
    - CONTEXT TO LOAD
    - THE WORK
    - AFTER
  optional:
    - VERIFICATION
```

---

## CONFIGURATION DEFAULTS

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| Ignore patterns | .ngram/config.yaml | Common patterns | Paths to skip in doctor |
| Monolith threshold | .ngram/config.yaml | 500 lines | SYNC archive trigger |
| Stale days | .ngram/config.yaml | 14 days | When SYNC is stale |
| Disabled checks | .ngram/config.yaml | [] | Doctor checks to skip |
