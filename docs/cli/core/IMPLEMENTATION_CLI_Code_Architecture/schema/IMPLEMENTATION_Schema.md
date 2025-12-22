# ngram Framework CLI — Implementation: Schema Definitions for CLI Flows

```
STATUS: STABLE
CREATED: 2025-12-18
```

---

## CHAIN

```
PATTERNS:        ../../PATTERNS_Why_CLI_Over_Copy.md
BEHAVIORS:       ../../BEHAVIORS_CLI_Command_Effects.md
ALGORITHM:       ../../ALGORITHM_CLI_Command_Execution_Logic/ALGORITHM_Overview.md
VALIDATION:      ../../VALIDATION_CLI_Instruction_Invariants.md
IMPLEMENTATION:  ../overview/IMPLEMENTATION_Overview.md
HEALTH:          ../../HEALTH_CLI_Command_Test_Coverage.md
SYNC:            ../../SYNC_CLI_Development_State.md
```

---

## CONTEXT

Defines the principal data structures shared across CLI commands, doctor checks, and reports.

---

## CODE STRUCTURE

This schema module describes structures used by `doctor`, `repair`, and `validate` commands, and aligns with the `../structure/IMPLEMENTATION_Code_Structure.md` file so the doc chain stays traceable.

## DESIGN PATTERNS

- **Data contracts**: Each structure (`ValidationResult`, `DoctorIssue`, etc.) acts as an immutable contract between CLI commands and health checks.
- **Flow coupling**: Schemas accompany flows described in the runtime doc to ensure consistent fields across modules.

## SCHEMA

### `ValidationResult`

```yaml
ValidationResult:
  required:
    - name: str
    - status: str           # PASS | WARN | FAIL
    - errors: list[str]
  optional:
    - severity: str
    - docs: list[str]
  constraints:
    - status in [PASS, WARN, FAIL]
```

### `DoctorIssue`

```yaml
DoctorIssue:
  required:
    - id: str
    - title: str
    - severity: str         # critical | warning | info
    - location: str
  optional:
    - doc: str
    - code: str
    - category: str
  relationships:
    - relates_to: RepairInstruction
```

### `RepairResult`

```yaml
RepairResult:
  required:
    - issue_id: str
    - agent: str
    - success: bool
  optional:
    - output_path: str
    - report: str
  constraints:
    - success == True implies report exists
```

### `CommandDefinition`

```yaml
CommandDefinition:
  required:
    - name: str
    - handler: str
  optional:
    - requires_health: bool
    - view: str
```

## ENTRY POINTS

The above schemas are consumed by entrypoints such as `ngram/doctor.py::run_doctor()` (DoctorIssue), `ngram/repair.py::run_repair()` (RepairResult), and `ngram/validate.py::validate_protocol()` (ValidationResult). Each entrypoint also outlines the `CommandDefinition` metadata in `ngram/cli.py`.

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

`ValidationResult` flows from `ngram/validate.py` → `ngram/doctor.py` → `ngram/doctor_report.py`. `DoctorIssue` flows through `doctor_checks_*` modules into `...ngram/state/SYNC_Project_Health.md`. `RepairResult` flows from `ngram/repair.py` agents into the repair report (in `...ngram/state/`).

## LOGIC CHAINS

1. `ngram/validate.py` emits `ValidationResult` → aggregator prints summary → status updates.
2. `ngram/doctor.py` collects `DoctorIssue` objects → `ngram/doctor_report.py` renders health.
3. `ngram/repair.py` collects `RepairResult` per issue → `ngram/repair_report.py` writes Markdown.

## MODULE DEPENDENCIES

Main consumers: `ngram/validate.py`, `ngram/doctor.py`, `ngram/repair.py`, `ngram/doctor_report.py`, `ngram/repair_report.py`. Supporting modules: `ngram/doctor_checks_*`, `ngram/repair_instructions*`.

## STATE MANAGEMENT

Schemas persist via `...ngram/state/SYNC_Project_Health.md`, the repair report (in `...ngram/state/`), and `...ngram/state/repair_results/` (future). Each run writes a JSON view of the active data structures.

## RUNTIME BEHAVIOR

These structures are created when commands parse CLI args, validate, and emit outputs; the runtime doc describes the loops maintaining them.

## CONCURRENCY MODEL

`DoctorIssue` and `RepairResult` objects are aggregated concurrently as modules run in parallel (doctor checks, repair agents). Collections merge once each flow completes.

## CONFIGURATION

Validation and doctor flows respect the config file (in `.ngram/`) keys like `disabled_checks`, `monolith_lines`, and `stale_sync_days`, impacting which structures get produced or filtered.

## BIDIRECTIONAL LINKS

This schema doc is referenced by `ngram/doctor_report.py`, `ngram/repair_report.py`, and `ngram/validate.py` via `DOCS:` pointers, and links back to the runtime and structure docs above, keeping the doc-code chain intact.

## MARKERS

<!-- @ngram:todo Add JSON Schema exporter for these structures so external tools can validate CLI outputs. -->
<!-- @ngram:proposition Capture schema versioning metadata inside `.ngram/state` to ensure backward compatibility as structures evolve. -->
