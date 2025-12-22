# ngram Framework CLI — Implementation: Code Structure

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

Entry point: `../overview/IMPLEMENTATION_Overview.md`.

---

## CODE STRUCTURE

````
ngram/
├── `ngram/cli.py`
├── `ngram/init_cmd.py`
├── `ngram/validate.py`
├── `ngram/doctor.py`
├── `ngram/doctor_checks.py`
├── `ngram/doctor_checks_core.py`
├── `ngram/doctor_checks_metadata.py`
├── `ngram/doctor_checks_reference.py`
├── `ngram/doctor_checks_stub.py`
├── `ngram/doctor_checks_prompt_integrity.py`
├── `ngram/doctor_types.py`
├── `ngram/doctor_report.py`
├── `ngram/doctor_files.py`
├── `ngram/agent_cli.py`
├── `ngram/repair.py`
├── `ngram/repair_core.py`
├── `ngram/repair_report.py`
├── `ngram/repair_instructions.py`
├── `ngram/repair_instructions_docs.py`
├── `ngram/repair_escalation_interactive.py`
├── `ngram/solve_escalations.py`
├── `ngram/sync.py`
├── `ngram/context.py`
├── `ngram/prompt.py`
├── `ngram/project_map.py`
├── `ngram/project_map_html.py`
├── `ngram/repo_overview.py`
├── `ngram/repo_overview_formatters.py`
├── `ngram/github.py`
└── `ngram/core_utils.py`
```

## DESIGN PATTERNS

- **Command dispatcher** — separates parsing (`ngram/cli.py`) from execution (commands).
- **Check catalog** — each `doctor_checks_*` module owns a `doctor_check_*` function to keep the scope manageable.
- **Agent orchestration** — `ngram/repair.py` calls `ngram/agent_cli.py` to spawn and monitor repair agents consistently.

## SCHEMA

Key data structures such as `ValidationResult`, `DoctorIssue`, `RepairResult`, and `RepairInstruction` are defined in `../schema/IMPLEMENTATION_Schema.md`.

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `main()` | `ngram/cli.py:42` | `ngram` CLI |
| `run_doctor()` | `ngram/doctor.py:127` | `ngram doctor` |
| `run_repair()` | `ngram/repair.py:970` | `ngram repair` |
| `print_bootstrap_prompt()` | `ngram/prompt.py:30` | `ngram prompt` |
| `generate_repo_overview()` | `ngram/repo_overview.py:12` | `ngram overview` |

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

Flow descriptions mirror `../runtime/IMPLEMENTATION_Runtime_And_Dependencies.md`; the primary flows are macros for command dispatch and health reporting, docking to `...ngram/state/SYNC_Project_Health.md` and `docs/`.

## LOGIC CHAINS

1. CLI dispatch → module handler → health/repair outcomes.
2. Doctor checks → `...ngram/state/SYNC_Project_Health.md` → `ngram/doctor_report.py`.

## MODULE DEPENDENCIES

CLI (`ngram/cli.py`) → `ngram/doctor.py`, `ngram/repair.py`, `ngram/prompt.py`, `ngram/repo_overview.py`, `ngram/core_utils.py`. Doctor → `ngram/doctor_checks_*`, `ngram/doctor_report.py`. Repair → `ngram/repair_core.py`, `ngram/repair_instructions*`, `ngram/agent_cli.py`.

## STATE MANAGEMENT

State lives in `...ngram/state/` (health, archives), `.ngram/traces/`, and `modules.yaml`; commands write snapshots after every run for observability.

## RUNTIME BEHAVIOR

Initialization: parse args, load modules metadata.
Main loop: dispatch → run command → collect DoctorIssue/RepairResult → persist state.
Shutdown: flush logs, exit cleanly.

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| CLI commands | synchronous | run sequentially |
| Doctor checks | threaded per bundle | may parallelize independent checks |
| Repair agents | ThreadPoolExecutor | agent subprocesses run concurrently with output serialized |

## CONFIGURATION

| Config | File | Description |
|--------|------|-------------|
| `monolith_lines` | config file (in `.ngram/`) | threshold for splitting monolith files |
| `stale_sync_days` | config file (in `.ngram/`) | staleness threshold for SYNC files |
| `disabled_checks` | config file (in `.ngram/`) | list of doctor checks to skip |

## BIDIRECTIONAL LINKS

`ngram/cli.py` contains `DOCS:` references back to this doc, and this doc links forward to `../overview/IMPLEMENTATION_Overview.md` and the referred code in the responsibilities table to keep doc-code coupling clear.

## FILE RESPONSIBILITIES

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `ngram/cli.py` | Entry point, argument parsing | `main()` | ~290 | OK |
| `ngram/init_cmd.py` | Protocol initialization | `init_protocol()` | ~168 | OK |
| `ngram/validate.py` | Protocol invariant checking | `validate_protocol()` | ~712 | SPLIT |
| `ngram/doctor.py` | Health check orchestration | `run_doctor()` | ~211 | OK |
| `ngram/doctor_checks.py` | Core health checks | `doctor_check_*()` | ~1364 | SPLIT |
| `ngram/doctor_checks_content.py` | Content analysis checks | `doctor_check_doc_duplication()` | ~410 | OK |
| `ngram/doctor_checks_docs.py` | Documentation checks | `doctor_check_incomplete_chain()` | ~316 | OK |
| `ngram/doctor_checks_quality.py` | Code quality checks | `doctor_check_hardcoded_secrets()` | ~172 | OK |
| `ngram/doctor_checks_sync.py` | SYNC checks | `doctor_check_stale_sync()` | ~228 | OK |
| `ngram/doctor_types.py` | Type definitions | `DoctorIssue`, `DoctorConfig` | ~41 | OK |
| `ngram/doctor_report.py` | Report generation | `generate_health_markdown()` | ~465 | WATCH |
| `ngram/doctor_files.py` | File discovery | `find_source_files()` | ~321 | OK |
| `ngram/agent_cli.py` | Agent CLI wrapper | `build_agent_command()` | ~60 | OK |
| `ngram/repair.py` | Repair orchestration | `repair_command()` | ~1013 | SPLIT |
| `ngram/repair_core.py` | Repair models + helpers | `RepairResult` | ~693 | WATCH |
| `ngram/repair_report.py` | Repair report generation | `generate_final_report()` | ~305 | OK |
| `ngram/repair_instructions.py` | Code/test/config repair prompts | `get_issue_instructions()` | ~765 | WATCH |
| `ngram/repair_instructions_docs.py` | Doc-related repair prompts | `get_doc_instructions()` | ~492 | WATCH |
| `ngram/repair_escalation_interactive.py` | Interactive repair helpers | `resolve_escalation_interactive()` | ~372 | OK |
| `ngram/solve_escalations.py` | Marker scanner | `find_escalation_markers()` | ~70 | OK |
| `ngram/sync.py` | SYNC file management | `sync_command()` | ~346 | OK |
| `ngram/context.py` | Documentation discovery | `get_module_context()` | ~553 | WATCH |
| `ngram/prompt.py` | LLM prompt generation | `print_bootstrap_prompt()` | ~89 | OK |
| `ngram/project_map.py` | Terminal dependency map | `print_project_map()` | ~359 | OK |
| `ngram/project_map_html.py` | HTML export | `generate_html_map()` | ~315 | OK |
| `ngram/repo_overview.py` | Repo overview | `generate_repo_overview()` | ~754 | SPLIT |
| `ngram/repo_overview_formatters.py` | Overview formatting | `format_text_overview()` | ~264 | OK |
| `ngram/github.py` | GitHub API integration | `create_issues_for_findings()` | ~288 | OK |
| `ngram/core_utils.py` | Shared helpers | `get_templates_path()` | ~103 | OK |

**Size Thresholds:**
- **OK** (<400 lines)
- **WATCH** (400-700 lines)
- **SPLIT** (>700 lines)

**GAPS**
- `ngram/doctor_checks.py` (~1364L) still needs further splitting.
- `ngram/validate.py` (~712L) needs check extraction.

**GAPS / IDEAS / QUESTIONS**
<!-- @ngram:todo Monitor `ngram/repair.py` for growth above 700 lines and extract new helpers if needed. -->
<!-- @ngram:proposition Provide an auto-generated summary of file statuses for doctors to reference. -->
