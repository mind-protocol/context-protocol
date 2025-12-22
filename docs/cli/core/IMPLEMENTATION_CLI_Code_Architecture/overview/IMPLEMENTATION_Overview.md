# ngram Framework CLI — Implementation: Code Architecture and Structure (Overview)

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
THIS:            ./IMPLEMENTATION_Overview.md
HEALTH:          ../../HEALTH_CLI_Command_Test_Coverage.md
SYNC:            ../../SYNC_CLI_Development_State.md
```

---

## OVERVIEW

The CLI is a modular command suite. Each subcommand lives in its own module and is dispatched by `ngram/cli.py`. The two largest subsystems are Doctor (health checks) and Repair (agent orchestration).

**Implementation sections:**
- `../structure/IMPLEMENTATION_Code_Structure.md`
- `../runtime/IMPLEMENTATION_Runtime_And_Dependencies.md`
- `../schema/IMPLEMENTATION_Schema.md`

---

## DESIGN PATTERNS

- **Command pattern** for argparse routing (`*_command()` functions).
- **Composition** for doctor checks (`doctor_check_*`).
- **Factory-style dispatch** for repair instruction generation.
- **Subprocess isolation** for agent execution.

**Boundaries:**
- Doctor subsystem: `ngram/doctor.py`, `ngram/doctor_checks_*` modules.
- Repair subsystem: `ngram/repair.py`, `ngram/repair_core.py` modules.
- File discovery: `ngram/doctor_files.py`, `ngram/core_utils.py`.

## SUBSYSTEM IMPLEMENTATIONS

| Subsystem | Files | Description |
|-----------|-------|-------------|
| Doctor core | `ngram/doctor.py`, `ngram/doctor_checks.py`, `ngram/doctor_checks_*`, `ngram/doctor_files.py` | CLI entry (`DoctorRunner`), check catalog, and discovery helpers powering `ngram doctor`. |
| Repair pipeline | `ngram/repair_core.py`, `ngram/repair_escalation_interactive.py`, `ngram/repair_instructions.py`, `ngram/repair_instructions_docs.py`, `ngram/repair_report.py` | Orchestrates agent repair flows, escalation UI, and remediation doc generation. |
| Repository overview | `ngram/repo_overview.py`, `ngram/repo_overview_formatters.py` | Generates project maps and README summaries referenced by doc navigation health indicators. |
| Escalation solver | `ngram/solve_escalations.py` | Prior stores escalate markers and surfaces proposals for humans/agents. |
| Core utilities | `ngram/core_utils.py` | Shared helpers for path resolution, doc discovery, JSON/YAML handling, and canonical file operations. |
| Refactor pipeline | `ngram/refactor.py` | Automates renaming/moving doc modules and regenerates overview/doctor outputs to keep the documentation graph consistent. |

```
IMPL: ngram/doctor.py
IMPL: ngram/doctor_checks.py
IMPL: ngram/doctor_checks_content.py
IMPL: ngram/doctor_checks_docs.py
IMPL: ngram/doctor_checks_quality.py
IMPL: ngram/doctor_checks_naming.py
IMPL: ngram/doctor_checks_sync.py
IMPL: ngram/doctor_files.py
IMPL: ngram/repair_core.py
IMPL: ngram/repair_escalation_interactive.py
IMPL: ngram/repair_instructions.py
IMPL: ngram/repair_instructions_docs.py
IMPL: ngram/repair_report.py
IMPL: ngram/repo_overview.py
IMPL: ngram/repo_overview_formatters.py
IMPL: ngram/solve_escalations.py
IMPL: ngram/core_utils.py
```

---

## BIDIRECTIONAL LINKS (ENTRY)

- `ngram/cli.py` includes a `DOCS:` pointer to `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md`.

---

## CODE STRUCTURE

The detailed file layout is captured in `../structure/IMPLEMENTATION_Code_Structure.md`; refer there for line counts and split candidates.

## SCHEMA

See `../schema/IMPLEMENTATION_Schema.md` for rich schema definitions (ValidationResult, DoctorIssue, RepairResult) used across CLI flows.

## ENTRY POINTS

Core entrypoints include `ngram/cli.py::main`, `ngram/doctor.py::run_doctor`, and `ngram/repair.py::run_repair`; nested commands read from `modules.yaml` to check doc ownership before executing.

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

Flows are described in `../runtime/IMPLEMENTATION_Runtime_And_Dependencies.md`; the biggest ones are command dispatch and health reporting. Each flow lists docking points for `.ngram/state` and `doc` artifacts.

## LOGIC CHAINS

Logic chains such as CLI dispatch → doctor runner → SYNC update are summarized in `../structure/IMPLEMENTATION_Code_Structure.md`, linking each step to doc anchors for traceability.

## MODULE DEPENDENCIES

Internal dependencies (CLI → doctor → repair, etc.) are captured in the runtime doc, while `modules.yaml` records how the CLI core relies on prompt + repo_overview modules.

## STATE MANAGEMENT

State layers include `...ngram/state/` (health reports), `.ngram/traces/`, and `modules.yaml`; the CLI writes them after each run to advertise progress to the doctor.

## RUNTIME BEHAVIOR

Runtime behavior splits across `ngram/cli.py` (parsing/dispatch) and each command module (doctor, repair, prompt); the runtime doc describes their initialization and exit flows.

## CONCURRENCY MODEL

The CLI itself is synchronous, but `repair` uses a `ThreadPoolExecutor` to manage agent subprocesses and `doctor_checks` parallelizes independent checks.

## CONFIGURATION

Key switches (monolith thresholds, disabled checks, agent timeouts) live in the config file (in `.ngram/`); the runtime doc references them with default values.

## BIDIRECTIONAL LINKS

Code references this overview via `DOCS:` markers inside `ngram/cli.py`, and the overview links back to key files listed above to ensure traceability.

## MARKERS

<!-- @ngram:todo Add DOCS: pointers from newly split doctor checks to this overview so each check is represented. -->
<!-- @ngram:proposition Provide a CLI command to regenerate this overview automatically after code moves. -->
## GAPS (ACTIVE)

### Extraction Candidates

- `ngram/doctor_checks.py` (~1364L) still needs further splitting.
- `ngram/validate.py` (~712L) needs check extraction.

### Missing Implementation

<!-- @ngram:todo Add type hints across the CLI codebase. -->
<!-- @ngram:todo Add DOCS: references to all source files. -->

---

## ARCHIVE POINTER

Older extraction history moved to `docs/cli/archive/SYNC_archive_2024-12.md` to keep this overview current.
