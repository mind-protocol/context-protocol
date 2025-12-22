# ngram Framework CLI — Implementation: Runtime and Dependencies

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

See `../structure/IMPLEMENTATION_Code_Structure.md` for the physical file layout, responsibilities, and split guidance. Runtime insights assume that structure stays roughly the same while doctor/repair modules evolve.

## DESIGN PATTERNS

- **Flow-based docking**: runtime flows focus on command dispatch plus health reporting to keep instrumentation visible.
- **Agent orchestration**: `ngram/repair.py` and `ngram/agent_cli.py` treat each agent invocation as an isolated subprocess with deterministic inputs/outputs.
- **Command dispatcher**: `ngram/cli.py` resolves subcommands by mapping names to handler modules, avoiding hardwired switches.

## SCHEMA

Schema definitions live in `../schema/IMPLEMENTATION_Schema.md`. Runtime flows rely on `ValidationResult`, `DoctorIssue`, and `RepairResult` to carry status through the flows described below.

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| main | ngram/cli.py:43 | `ngram` command |
| init_protocol | ngram/init_cmd.py:15 | `ngram init` |
| validate_protocol | ngram/validate.py:667 | `ngram validate` |
| doctor_command | ngram/doctor.py:127 | `ngram doctor` |
| repair_command | ngram/repair.py:970 | `ngram repair` |
| sync_command | ngram/sync.py | `ngram sync` |
| print_module_context | ngram/context.py:442 | `ngram context` |
| print_bootstrap_prompt | ngram/prompt.py | `ngram prompt` |
| print_project_map | ngram/project_map.py | `ngram overview` |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

- **Command dispatch flow:** `ngram/cli.py` parses args → selects handler → writes outputs to stdout/files → writes SYNC/state artifacts.
- **Health flow:** `ngram/doctor.py` collects issues → `ngram/doctor_report.py` renders Markdown + JSON → writes `...ngram/state/SYNC_Project_Health.md` and archives.
- **Repair flow:** `ngram/repair.py` builds prompts → `ngram/agent_cli.py` runs subprocesses → `ngram/repair_report.py` emits artifacts plus the repair report (in `...ngram/state/`).
- **Init flow:** `ngram/init_cmd.py` copies protocol assets → writes AGENTS/CLAUDE → copies `.ngram/skills` into `.claude/skills` and `$CODEX_HOME/skills`.

Docking points include `...ngram/state/`, `.ngram/traces/`, `docs/`, and `...ngram/state/SYNC_Project_Health.md`.

## LOGIC CHAINS

1. CLI dispatch → module handler → `DoctorIssue`/`RepairResult` → final report.
2. Health runner → `ngram/doctor_report.py` → `...ngram/state/SYNC_Project_Health.md` + Markdown + JSON outputs.

---

## MODULE DEPENDENCIES

Internal: CLI → doctor, repair, prompt, repo_overview, core_utils. Doctor → `doctor_checks_*`, `doctor_report`, `doctor_files`. Repair → `ngram/repair_core`, `ngram/repair_instructions`, `ngram/agent_cli`. External: `argparse`, `pathlib`, `subprocess`, `yaml`, `json`.

## STATE MANAGEMENT

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Doctor config | `DoctorConfig` | per-command | in-memory |
| Validation results | `List[ValidationResult]` | per-command | in-memory |
| Repair results | `List[RepairResult]` | per-command | in-memory |
| Trace logs | `.ngram/traces/` | persistent | rotates daily |
| Health report | `...ngram/state/SYNC_Project_Health.md` | persistent | overwritten each run |

## RUNTIME BEHAVIOR

```
1. argparse parses sys.argv
2. Router dispatches to command function
3. Command loads config if needed
4. Command executes
5. Results printed/saved
6. sys.exit(code)
```

### Agent Execution (repair)

```
1. Build prompt from issue + instructions
2. Spawn agent subprocess via `ngram/agent_cli.py` wrapper
3. Stream JSON (Claude) or text (Codex/Gemini)
4. Wait for completion or timeout
5. Return RepairResult
```

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| CLI commands | synchronous | run sequentially |
| Doctor checks | threaded | `doctor_checks_core` runs bundles in parallel |
| Repair agents | ThreadPoolExecutor | guard output with print_lock |

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `monolith_lines` | config file (in `.ngram/`) | 500 | Monolith threshold |
| `stale_sync_days` | config file (in `.ngram/`) | 14 | SYNC staleness |
| `ignore` | config file (in `.ngram/`) + `.gitignore` | common | Ignore patterns |
| `disabled_checks` | config file (in `.ngram/`) | [] | Checks to skip |
| `svg_namespace` | config file (in `.ngram/`) or `NGRAM_SVG_NAMESPACE` | http://www.w3.org/2000/svg | Project map SVG namespace |

## BIDIRECTIONAL LINKS

`ngram/cli.py` and command modules contain `DOCS:` pointers to this file; the file also links back to `../overview/IMPLEMENTATION_Overview.md` and the entry point files listed above to keep doc-code coherence.

## MARKERS

<!-- @ngram:todo Capture runtime telemetry (command durations, doctor coverage) in `.ngram/state`. -->
<!-- @ngram:proposition Add CLI telemetry for frequent commands to feed into future architecture docs. -->
