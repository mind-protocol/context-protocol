# ngram Framework CLI — Implementation: Code Architecture and Structure

```
STATUS: STABLE
CREATED: 2025-12-18
```

---

## CHAIN

```
PATTERNS:        ./core/PATTERNS_Why_CLI_Over_Copy.md
BEHAVIORS:       ./core/BEHAVIORS_CLI_Command_Effects.md
ALGORITHM:       ./ALGORITHM_CLI_Command_Execution_Logic.md
VALIDATION:      ./core/VALIDATION_CLI_Instruction_Invariants.md
THIS:            docs/cli/IMPLEMENTATION_CLI_Code_Architecture.md
HEALTH:          ./core/HEALTH_CLI_Command_Test_Coverage.md
SYNC:            ./core/SYNC_CLI_Development_State.md

IMPL:            ngram/cli.py
IMPL:            ngram/doctor.py
IMPL:            ngram/repair.py
IMPL:            ngram/prompt.py
```

> **Contract:** Read the chain before updating. Keep this overview aligned with the detailed subdocs in `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/`.

---

## CODE STRUCTURE

```
ngram/
├── ngram/cli.py                      # single CLI entrypoint that routes into each command
├── init_cmd.py                 # protocol initialization helpers
├── validate.py                 # invariants enforcement command
├── doctor.py                   # health orchestration entrypoint
├── doctor_checks.py            # aggregated doctor checks
├── doctor_checks_core.py       # orchestrates check bundles
├── doctor_checks_metadata.py   # metadata-driven helpers
├── doctor_checks_reference.py  # reference-based helpers
├── doctor_checks_stub.py       # placeholder/stub checks
├── doctor_checks_prompt_integrity.py # prompt integrity helpers
├── doctor_report.py            # report generation
├── doctor_files.py             # doc discovery
├── repair.py                   # agent orchestration CLI interface
├── repair_core.py              # repair models and helpers
├── repair_instructions.py      # prompt generation
├── repair_instructions_docs.py # doc scaffolding for repairs
├── repair_escalation_interactive.py # interactive escalation helpers
├── repo_overview.py            # project-map generation
├── repo_overview_formatters.py # formatting helpers for overviews
├── solve_escalations.py        # marker scanner
├── core_utils.py               # shared utilities for doc discovery and JSON/YAML
├── ngram/prompt.py                   # bootstrap prompt generation for agents
├── project_map.py              # repo overview command
└── project_map_html.py         # HTML export
```

This split is described in `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/structure/IMPLEMENTATION_Code_Structure.md` along with file responsibilities and status indicators (OK/WATCH/SPLIT).

---

## DESIGN PATTERNS

- **Command pattern** for `ngram/cli.py` routing and ensuring each subcommand implements a `run()` style function.
- **Monolith decomposition** documented in `doctor_checks` submodules to keep each health check self-contained (see ideas in the submodule GAPS).
- **Flow-based docking** described in the subdocs to ensure repair, doctor, and prompt flows expose explicit hooks for health observers.

Anti-pattern guardrails:
- **God objects** are avoided by splitting `doctor_checks` into `core`, `metadata`, and `reference` helpers as noted in the core doc chain.
- **Premature optimization**: new limits go into the config file (in `.ngram/`) only when validated by DOC_TEMPLATE_DRIFT insights.

Boundaries:
| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Health checks | `ngram/doctor.py` plus `ngram/doctor_checks_*` modules | CLI routing logic | `run_doctor()` |
| Repair agents | `ngram/repair.py` plus `ngram/repair_core.py` and instruction modules | CLI routing logic | `run_repair()` |
| Prompt provisioning | `ngram/prompt.py` | command parsing | `print_bootstrap_prompt()` |

---

## SCHEMA

```yaml
ValidationResult:
  required:
    - name: str           # refer to docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/schema/IMPLEMENTATION_Schema.md for fields
    - errors: list[str]
  optional:
    - severity: str
  constraints:
    - severity must be one of INFO|WARN|FAIL

DoctorIssue:
  required:
    - id: str
    - category: str
  optional:
    - doc: str
  relationships:
    - relates_to: RepairInstruction
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| `main()` | `ngram/cli.py:42` | `ngram` command |
| `init_protocol()` | `ngram/init_cmd.py:10` | `ngram init` |
| `validate_protocol()` | `ngram/validate.py:667` | `ngram validate` |
| `run_doctor()` | `ngram/doctor.py:127` | `ngram doctor` |
| `run_repair()` | `ngram/repair.py:970` | `ngram repair` |
| `print_bootstrap_prompt()` | `ngram/prompt.py:30` | `ngram prompt` |
| `generate_repo_overview()` | `ngram/repo_overview.py:12` | `ngram repo-overview` |

---

## DATA FLOW AND DOCKING (FLOW-BY-FLOW)

### Command Dispatch Flow: parse → route → execute

Purpose: translates CLI input into command executions, ensuring each flow routes through health hooks.

```yaml
flow:
  name: command_dispatch
  purpose: route argv into validated CLI commands
  scope: argv → command module → stdout/files
  steps:
    - id: parse_args
      description: argparse inspects sys.argv and applies subcommand definitions
      file: ngram/cli.py
      function: main
      input: sys.argv
      output: command_name, parsed_args
      trigger: CLI invocation
      side_effects: may set logging config
    - id: select_module
      description: router resolves the command name to the implementer in doctor/repair/prompt
      file: ngram/cli.py
      function: dispatch_command
      input: command_name, parsed_args
      output: selected module callable
      trigger: after parser completes
      side_effects: none
    - id: execute
      description: runs the selected command, which in turn may call doctor, repair, or prompt helpers
      file: {doctor.py | repair.py | ngram/prompt.py}
      function: run_doctor/run_repair/print_bootstrap_prompt
      input: parsed_args
      output: exit code, artifacts
      trigger: dispatch_command
      side_effects: writes SYNC, state files, report artifacts
  docking_points:
    guidance:
      include_when: targeted health entry point or heavy flow
      omit_when: trivial helper command
    available:
      - id: doc_sync
        type: file
        direction: output
        file: ...ngram/state/SYNC_Project_Health.md
        function: doctor_runner
        trigger: after doctor finishes
        payload: JSON
        async_hook: not_applicable
        needs: none
      - id: repair_report
        type: event
        direction: output
        file: ngram/repair_report.py
        function: generate_final_report
        trigger: post repair agents
        payload: Markdown report
        async_hook: optional
        needs: journaling, timestamping
    health_recommended:
      - dock_id: doc_sync
        reason: captures health run results for monitoring

### Health Check Flow: doctor → checks → reports

Purpose: orchestrate the health analysis pipeline, ensuring each step updates `.ngram/state` and surfaces doc-link integrity.

```yaml
flow:
  name: doctor_health
  purpose: run the doctor checks and surface reports for health tracking
  scope: docs → doctor modules → output artifacts
  steps:
    - id: load_context
      description: gather module mappings, sync files, and config to seed the checks
      file: ngram/context.py
      function: get_module_context
      input: modules.yaml, docs/, ...ngram/state/
      output: context bundle
      trigger: start of doctor run
      side_effects: none
    - id: run_checks
      description: execute each `doctor_check_*` function to collect issues
      file: ngram/doctor_checks_core.py
      function: doctor_check_bundle
      input: context bundle
      output: list of DoctorIssue
      trigger: after context load
      side_effects: may log intermediate signals
    - id: render_report
      description: aggregate issues into markdown/JSON for CLI output and STATE files
      file: ngram/doctor_report.py
      function: generate_health_markdown
      input: list of DoctorIssue
      output: Markdown + JSON + ...ngram/state/SYNC_Project_Health.md
      trigger: after checks complete
      side_effects: writes health state
```

---

## LOGIC CHAINS

### LC1: Command-to-health handshake

**Purpose:** Guarantee that every CLI command touches health state in a predictable way.

```
sys.argv
  → ngram/cli.py.dispatch_command()
    → {doctor.run_doctor() | repair.run_repair() | prompt.print_bootstrap_prompt()}
      → health artifacts (.ngram/state, docs, reports)
```

**Data transformation:**
- Input: parsed CLI args → ensures command name and options.
- After dispatch: enriched context with module metadata.
- Output: `DoctorIssue` or `RepairResult` for downstream consumers.

### LC2: Health-report rendering

**Purpose:** Translate collected DoctorIssue objects into human-readable signals.

```
DoctorIssue list
  → ngram/doctor_report.py.generate_health_markdown()
    → markdown + JSON + .ngram/state reports
```

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
ngram/cli.py
  └── imports → doctor.py, repair.py, ngram/prompt.py, core_utils.py
doctor.py
  └── imports → doctor_checks_core.py, ngram/doctor_checks_metadata.py, doctor_report.py
repair.py
  └── imports → repair_core.py, repair_instructions_docs.py, agent_cli.py
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| `argparse` | CLI parsing | `ngram/cli.py` |
| `json` | State/output serialization | `ngram/core_utils.py` |
| `yaml` | Template loading/config | `ngram/context.py`, `ngram/init_cmd.py` |

Repair agent threading relies on a thread pool inside `ngram/repair.py` so subprocess output is serialized while checks continue.

---

## STATE MANAGEMENT

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Health report | `...ngram/state/SYNC_Project_Health.md` | project | overwritten each `ngram doctor` |
| Doc templates | `docs/` | project | updated when templates change |
| Module map | `modules.yaml` | project | edited when modules move |
| Repair results | `...ngram/state/repair_results/` (future) | per run | appended per repair |

State transitions:

```
raw CLI args ──> dispatch context ──> command execution ──> issue artifacts ──> health report
```

---

## RUNTIME BEHAVIOR

### Initialization

```
1. Parse CLI args via argparse
2. Instantiate logging and config
3. Load module manifest
```

### Main Cycle

```
1. Dispatch command
2. Run doctor/repair/prompt
3. Print output and write SYNC/state files
4. Exit with result
```

### Shutdown

```
1. Flush logs/reports
2. Save final state (.ngram/state)
3. Exit with code
```

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| CLI commands | synchronous | Each command runs to completion before exit |
| Doctor checks | threaded | `doctor_checks_core` may parallelize per check bundle |
| Repair agents | `ThreadPoolExecutor` | Tracks agent subprocess output streams |

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| `monolith_lines` | config file (in `.ngram/`) | `500` | When to split files before checking |
| `stale_sync_days` | config file (in `.ngram/`) | `14` | Stale SYNC threshold before warning |
| `disabled_checks` | config file (in `.ngram/`) | `[]` | Doctor checks to skip |
| `svg_namespace` | config file (in `.ngram/`) | `http://www.w3.org/2000/svg` | Namespace for project map exports |

---

## BIDIRECTIONAL LINKS

### Code → Docs

| File | Line | Reference |
|------|------|-----------|
| `ngram/cli.py` | ~40 | `docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md` |
| `ngram/doctor.py` | ~120 | `docs/cli/core/IMPLEMENTATION_CLI_Code_Architecture/overview/IMPLEMENTATION_Overview.md` |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| Command dispatch flow | `ngram/cli.py::dispatch_command` |
| Health runner | `ngram/doctor.py::run_doctor` |

---

## MARKERS

### Extraction Candidates

| File | Current | Target | Extract To | Notes |
|------|---------|--------|------------|-------|
| `ngram/doctor_checks_core.py` | ~800L | <400L | `ngram/doctor_checks_metadata.py` | Completed split but watch for growth |
| `ngram/repair.py` | ~1200L | <700L | `ngram/repair_core.py` | Agent orchestration still heavy |

### Missing Implementation

<!-- @ngram:todo Add DOCS pointers to `ngram/prompt.py` and `ngram/doctor_checks_*` in each submodule. -->
<!-- @ngram:todo Ensure `ngram/repair.py` writes to `...ngram/state/repair_results/` (future work). -->

### Ideas

<!-- @ngram:proposition Introduce a metadata-first doc when splitting new CLI modules. -->
<!-- @ngram:proposition Surface prompt health data directly in `ngram doctor` output for faster operator triage. -->

### Questions

<!-- @ngram:escalation Should `ngram/doctor_files.py` be split further or removed once new discovery helpers cover the same ground? -->
<!-- @ngram:escalation How do we keep `modules.yaml` in sync when new CLI commands land? -->
