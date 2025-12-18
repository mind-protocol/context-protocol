# ADD Framework CLI — Implementation: Code Architecture and Structure

```
STATUS: STABLE
CREATED: 2025-12-18
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Why_CLI_Over_Copy.md
BEHAVIORS:       ./BEHAVIORS_CLI_Command_Effects.md
ALGORITHM:       ./ALGORITHM_CLI_Logic.md
VALIDATION:      ./VALIDATION_CLI_Invariants.md
THIS:            IMPLEMENTATION_CLI_Code_Architecture.md (you are here)
TEST:            ./TEST_CLI_Coverage.md
SYNC:            ./SYNC_CLI_State.md
```

---

## CODE STRUCTURE

```
src/ngram/
├── __init__.py             # Package init
├── cli.py                  # Entry point, argparse routing
├── init_cmd.py             # Init command implementation
├── validate.py             # Validation checks
├── doctor.py               # Health check orchestration (slim)
├── doctor_checks.py        # Health check functions (core)
├── doctor_checks_content.py # Content analysis checks (extracted)
├── doctor_types.py         # DoctorIssue, DoctorConfig types
├── doctor_report.py        # Report generation, scoring
├── doctor_files.py         # File discovery utilities
├── repair.py               # Agent orchestration for repairs
├── repair_report.py        # Repair report generation (LLM + template)
├── repair_instructions.py  # Code/test/config repair prompts (main)
├── repair_instructions_docs.py # Doc-related repair prompts (extracted)
├── sync.py                 # SYNC file management
├── context.py              # Code-to-docs navigation
├── prompt.py               # Bootstrap prompt generation
├── project_map.py          # Visual dependency map (terminal)
├── project_map_html.py     # HTML export for project map
├── github.py               # GitHub issue integration
└── utils.py                # Shared utilities
```

**Logical Groupings** (all in `src/ngram/`):
- **Doctor subsystem:** doctor, doctor_checks, doctor_checks_content, doctor_types, doctor_report, doctor_files
- **Repair subsystem:** repair, repair_core, repair_report, repair_instructions, repair_instructions_docs
- **Project map:** project_map, project_map_html

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `src/ngram/cli.py` | Entry point, argument parsing | `main()` | ~290 | OK |
| `src/ngram/init_cmd.py` | Protocol initialization | `init_protocol()` | ~168 | OK |
| `src/ngram/validate.py` | Protocol invariant checking | `validate_protocol()`, `ValidationResult` | ~712 | SPLIT |
| `src/ngram/doctor.py` | Health check orchestration | `run_doctor()`, `doctor_command()` | ~211 | OK |
| `src/ngram/doctor_checks.py` | Health check functions (core) | `doctor_check_*()` (20 functions) | ~1364 | SPLIT |
| `src/ngram/doctor_checks_content.py` | Content analysis checks | `doctor_check_doc_duplication()`, `doctor_check_new_undoc_code()`, `doctor_check_long_strings()` | ~410 | OK |
| `src/ngram/doctor_types.py` | Type definitions | `DoctorIssue`, `DoctorConfig` | ~41 | OK |
| `src/ngram/doctor_report.py` | Report generation | `generate_health_markdown()`, `calculate_health_score()` | ~465 | WATCH |
| `src/ngram/doctor_files.py` | File discovery | `find_source_files()`, `find_code_directories()` | ~321 | OK |
| `src/ngram/repair.py` | Repair orchestration | `repair_command()`, `spawn_repair_agent()` | ~1013 | SPLIT |
| `src/ngram/repair_report.py` | Report generation | `generate_llm_report()`, `generate_final_report()` | ~305 | OK |
| `src/ngram/repair_instructions.py` | Code/test/config repair prompts | `get_issue_instructions()` | ~765 | WATCH |
| `src/ngram/repair_instructions_docs.py` | Doc-related repair prompts | `get_doc_instructions()` | ~492 | WATCH |
| `src/ngram/sync.py` | SYNC file management | `sync_command()`, `archive_all_syncs()` | ~346 | OK |
| `src/ngram/context.py` | Documentation discovery | `print_module_context()`, `get_module_context()` | ~553 | WATCH |
| `src/ngram/prompt.py` | LLM prompt generation | `print_bootstrap_prompt()` | ~89 | OK |
| `src/ngram/project_map.py` | Terminal dependency map | `print_project_map()` | ~359 | OK |
| `src/ngram/project_map_html.py` | HTML export | `generate_html_map()` | ~315 | OK |
| `src/ngram/github.py` | GitHub API integration | `create_issues_for_findings()` | ~288 | OK |
| `src/ngram/utils.py` | Shared helpers | `get_templates_path()`, `find_module_directories()` | ~103 | OK |

**Size Thresholds:**
- **OK** (<400 lines): Healthy size
- **WATCH** (400-700 lines): Monitor for extraction opportunities
- **SPLIT** (>700 lines): Requires splitting

---

## DESIGN PATTERNS

### Architecture Pattern

**Pattern:** Modular CLI with Command Pattern

**Why:** Each CLI subcommand is an independent module. Repair uses subprocess spawning for agent isolation. Doctor uses composition of check functions.

### Code Patterns in Use

| Pattern | Applied To | Purpose |
|---------|------------|---------|
| Command Pattern | cli module → each `*_command()` | Dispatch based on argparse |
| Composition | doctor module → `doctor_check_*()` | Combine independent health checks |
| Factory | repair_instructions module | Generate prompts per issue type |
| Subprocess Isolation | repair module → `spawn_repair_agent()` | Each agent runs independently |

### Anti-Patterns to Avoid

- **God Object**: doctor and repair modules are currently too large - need continued extraction
- **Copy-Paste**: Don't duplicate check logic; compose check functions instead
- **Premature Abstraction**: Don't create base classes until 3+ similar implementations

### Boundaries

| Boundary | Inside | Outside | Interface |
|----------|--------|---------|-----------|
| Doctor subsystem | doctor_* modules | Other commands | `run_doctor()`, `DoctorIssue` |
| Repair subsystem | repair_* modules | Other commands | `repair_command()`, `RepairResult` |
| File discovery | doctor_files, utils | Check logic | `find_source_files()`, `find_code_directories()` |

---

## SCHEMA

### DoctorIssue

```yaml
DoctorIssue:
  required:
    - issue_type: str     # MONOLITH, UNDOCUMENTED, etc.
    - severity: str       # critical, warning, info
    - path: str           # Relative path to affected file/dir
    - message: str        # Human-readable description
  optional:
    - details: Dict       # Issue-specific metadata
    - suggestion: str     # Recommended fix action
```

### ValidationResult

```yaml
ValidationResult:
  required:
    - check_id: str       # V1, V2, FC, NC, MM, etc.
    - name: str           # Human-readable check name
    - passed: bool        # Did check pass?
    - message: str        # Summary message
    - details: List[str]  # Detailed findings
```

### RepairResult

```yaml
RepairResult:
  required:
    - issue_type: str
    - target_path: str
    - success: bool
    - agent_output: str
    - duration_seconds: float
  optional:
    - error: str          # Error message if failed
```

---

## ENTRY POINTS

| Entry Point | File:Line | Triggered By |
|-------------|-----------|--------------|
| main | src/ngram/cli.py:43 | ngram command |
| init_protocol | src/ngram/init_cmd.py:15 | ngram init |
| validate_protocol | src/ngram/validate.py:667 | ngram validate |
| doctor_command | src/ngram/doctor.py:127 | ngram doctor |
| repair_command | src/ngram/repair.py:970 | ngram repair |
| sync_command | src/ngram/sync.py | ngram sync |
| print_module_context | src/ngram/context.py:442 | ngram context |
| print_bootstrap_prompt | src/ngram/prompt.py | ngram prompt |
| print_project_map | src/ngram/project_map.py | ngram map |

---

## DATA FLOW

For detailed algorithmic steps, see `docs/cli/ALGORITHM_CLI_Logic.md`.

**Summary:**
- **Init:** `get_templates_path()` → `shutil.copytree()` → update CLAUDE.md
- **Doctor:** `load_config()` → 12 health checks → `calculate_health_score()` → write report
- **Repair:** `run_doctor()` → filter issues → parallel agents → re-check → report

---

## MODULE DEPENDENCIES

### Internal Dependencies

```
cli.py
    └── imports → init_cmd.py
    └── imports → validate.py
    └── imports → doctor.py
    └── imports → repair.py
    └── imports → sync.py
    └── imports → context.py
    └── imports → prompt.py
    └── imports → project_map.py

doctor.py
    └── imports → doctor_checks.py (20 doctor_check_*() functions)
    └── imports → doctor_checks_content.py (3 content analysis check functions)
    └── imports → doctor_types.py (DoctorIssue, DoctorConfig)
    └── imports → doctor_report.py (generate_health_markdown, print_doctor_report)
    └── imports → doctor_files.py (load_doctor_config, load_doctor_ignore)
    └── imports → sync.py

doctor_checks.py
    └── imports → doctor_types.py (DoctorIssue, DoctorConfig)
    └── imports → doctor_files.py (should_ignore_path, find_source_files, etc.)
    └── imports → utils.py

doctor_checks_content.py
    └── imports → doctor_types.py (DoctorIssue, DoctorConfig)
    └── imports → doctor_files.py (should_ignore_path, find_source_files, count_lines)
    └── imports → utils.py (find_module_directories)

repair.py
    └── imports → doctor.py (run_doctor, DoctorIssue)
    └── imports → repair_core.py (RepairResult, ArbitrageDecision, constants)
    └── imports → repair_report.py (generate_llm_report, generate_final_report)
    └── imports → repair_instructions.py (get_issue_instructions)

repair_instructions.py
    └── imports → doctor.py (DoctorIssue)
    └── imports → repair_instructions_docs.py (get_doc_instructions)

repair_instructions_docs.py
    └── imports → doctor.py (DoctorIssue)

repair_report.py
    └── imports → repair_core.py (RepairResult)

project_map.py
    └── imports → project_map_html.py (generate_html_map)

validate.py
    └── imports → utils.py
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| argparse | CLI parsing | cli |
| pathlib | File paths | All modules |
| subprocess | Agent spawning | repair |
| concurrent.futures | Parallel execution | repair |
| yaml (optional) | modules.yaml parsing | utils, doctor |
| json | JSON output, traces | doctor, context |
| shutil | File copying | init_cmd |
| re | Regex patterns | validate, doctor |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Lifecycle |
|-------|----------|-------|-----------|
| Doctor config | `DoctorConfig` instance | Function call | Per-command |
| Validation results | `List[ValidationResult]` | Function call | Per-command |
| Repair results | `List[RepairResult]` | Function call | Per-command |
| Trace logs | `.ngram/traces/` | Persistent | Daily files |
| Health report | .ngram/state/SYNC_Project_Health.md | Persistent | Overwritten each run |

### State Transitions

```
Project → init → Protocol Installed → validate → Validated → doctor → Health Known
                                                                    ↓
                                                               repair → Fixed
```

---

## RUNTIME BEHAVIOR

### Initialization

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
2. Spawn claude subprocess with prompt
3. Stream JSON output, parse for text/tool_use
4. Show progress to user
5. Wait for completion or timeout
6. Check for REPAIR COMPLETE/FAILED markers
7. Return RepairResult
```

---

## CONCURRENCY MODEL

| Component | Model | Notes |
|-----------|-------|-------|
| CLI commands | sync | Single-threaded execution |
| Repair agents | threaded | ThreadPoolExecutor with N workers |
| Agent output | streaming | Real-time JSON parsing |

**Thread safety:**
- `print_lock` mutex for parallel agent output
- Each agent has isolated subprocess
- No shared mutable state between agents

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| monolith_lines | .ngram/config.yaml (optional) | 500 | Lines threshold for monolith detection |
| stale_sync_days | .ngram/config.yaml (optional) | 14 | Days before SYNC is stale |
| ignore | .ngram/config.yaml + .gitignore | common patterns | Paths to ignore |
| disabled_checks | .ngram/config.yaml (optional) | [] | Checks to skip |

---

## BIDIRECTIONAL LINKS

### Code → Docs

Files that reference this documentation:

| File | Line | Reference |
|------|------|-----------|
| src/ngram/cli.py | 4 | DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM: Validate | src/ngram/validate.py:667 |
| ALGORITHM: Doctor | src/ngram/doctor.py:1160 |
| ALGORITHM: Repair | src/ngram/repair.py:970 |
| BEHAVIOR B1: Init | src/ngram/init_cmd.py:15 |
| VALIDATION V1 | src/ngram/validate.py:33 |

---

## GAPS / IDEAS / QUESTIONS

### Extraction Candidates (Remaining)

Files at SPLIT status need continued decomposition:

| Current File | Lines | Target | Proposed New File | What to Move |
|--------------|-------|--------|-------------------|--------------|
| doctor_checks | ~1364L | <400L | doctor_checks_docs.py | Group remaining: doc checks, code checks, config checks |
| repair | ~1013L | <400L | repair_interactive (planned) | Interactive UI: `resolve_arbitrage_interactive()`, manager agent functions |
| validate | ~712L | <400L | validate_checks (planned) | Individual validation check functions |

### Completed Extractions

| Date | Source | Target | Lines Moved |
|------|--------|--------|-------------|
| 2025-12-18 | doctor.py (1900L) | doctor_checks.py | 23 check functions, ~1690L |
| 2025-12-18 | repair.py (1273L) | repair_report.py | Report generation: REPORT_PROMPT, generate_llm_report(), generate_final_report() ~260L |
| 2025-12-18 | doctor_checks.py (1738L) | doctor_checks_content.py | Content checks: doctor_check_doc_duplication, doctor_check_new_undoc_code, doctor_check_long_strings ~374L |
| 2025-12-18 | repair_instructions.py (1226L) | repair_instructions_docs.py | Doc instructions: UNDOCUMENTED, PLACEHOLDER, INCOMPLETE_CHAIN, NO_DOCS_REF, UNDOC_IMPL, ORPHAN_DOCS, LARGE_DOC_MODULE, DOC_GAPS, STALE_IMPL, DOC_DUPLICATION ~461L |

### Missing Implementation

- [ ] Add type hints throughout codebase
- [ ] Add DOCS: references to all source files

### Ideas (Not Yet Implemented)

- IDEA: Plugin system for custom checks
- IDEA: Agent prompt templates could be externalized to markdown files
- IDEA: Color/formatting utilities extracted to new file (formatting module)
