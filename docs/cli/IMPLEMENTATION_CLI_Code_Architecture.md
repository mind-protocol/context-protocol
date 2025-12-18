# Context Protocol CLI — Implementation: Code Architecture and Structure

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
src/context_protocol/
├── __init__.py             # Package init
├── cli.py                  # Entry point, argparse routing
├── init_cmd.py             # Init command implementation
├── validate.py             # Validation checks
├── doctor.py               # Health check orchestration (slim)
├── doctor_checks.py        # All health check functions
├── doctor_types.py         # DoctorIssue, DoctorConfig types
├── doctor_report.py        # Report generation, scoring
├── doctor_files.py         # File discovery utilities
├── repair.py               # Agent orchestration for repairs
├── repair_instructions.py  # Issue-specific repair prompts
├── sync.py                 # SYNC file management
├── context.py              # Code-to-docs navigation
├── prompt.py               # Bootstrap prompt generation
├── project_map.py          # Visual dependency map (terminal)
├── project_map_html.py     # HTML export for project map
├── github.py               # GitHub issue integration
└── utils.py                # Shared utilities
```

**Logical Groupings** (all in `src/context_protocol/`):
- **Doctor subsystem:** doctor, doctor_checks, doctor_types, doctor_report, doctor_files
- **Repair subsystem:** repair, repair_instructions
- **Project map:** project_map, project_map_html

### File Responsibilities

| File | Purpose | Key Functions/Classes | Lines | Status |
|------|---------|----------------------|-------|--------|
| `src/context_protocol/cli.py` | Entry point, argument parsing | `main()` | ~290 | OK |
| `src/context_protocol/init_cmd.py` | Protocol initialization | `init_protocol()` | ~168 | OK |
| `src/context_protocol/validate.py` | Protocol invariant checking | `validate_protocol()`, `ValidationResult` | ~712 | SPLIT |
| `src/context_protocol/doctor.py` | Health check orchestration | `run_doctor()`, `doctor_command()` | ~211 | OK |
| `src/context_protocol/doctor_checks.py` | Health check functions | `doctor_check_*()` (23 functions) | ~1732 | SPLIT |
| `src/context_protocol/doctor_types.py` | Type definitions | `DoctorIssue`, `DoctorConfig` | ~41 | OK |
| `src/context_protocol/doctor_report.py` | Report generation | `generate_health_markdown()`, `calculate_health_score()` | ~465 | WATCH |
| `src/context_protocol/doctor_files.py` | File discovery | `find_source_files()`, `find_code_directories()` | ~321 | OK |
| `src/context_protocol/repair.py` | Repair orchestration | `repair_command()`, `spawn_repair_agent()` | ~1333 | SPLIT |
| `src/context_protocol/repair_instructions.py` | Repair prompts | `get_issue_instructions()` | ~813 | SPLIT |
| `src/context_protocol/sync.py` | SYNC file management | `sync_command()`, `archive_all_syncs()` | ~346 | OK |
| `src/context_protocol/context.py` | Documentation discovery | `print_module_context()`, `get_module_context()` | ~553 | WATCH |
| `src/context_protocol/prompt.py` | LLM prompt generation | `print_bootstrap_prompt()` | ~89 | OK |
| `src/context_protocol/project_map.py` | Terminal dependency map | `print_project_map()` | ~359 | OK |
| `src/context_protocol/project_map_html.py` | HTML export | `generate_html_map()` | ~315 | OK |
| `src/context_protocol/github.py` | GitHub API integration | `create_issues_for_findings()` | ~288 | OK |
| `src/context_protocol/utils.py` | Shared helpers | `get_templates_path()`, `find_module_directories()` | ~103 | OK |

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
| main | src/context_protocol/cli.py:43 | context-protocol command |
| init_protocol | src/context_protocol/init_cmd.py:15 | context-protocol init |
| validate_protocol | src/context_protocol/validate.py:667 | context-protocol validate |
| doctor_command | src/context_protocol/doctor.py:127 | context-protocol doctor |
| repair_command | src/context_protocol/repair.py:970 | context-protocol repair |
| sync_command | src/context_protocol/sync.py | context-protocol sync |
| print_module_context | src/context_protocol/context.py:442 | context-protocol context |
| print_bootstrap_prompt | src/context_protocol/prompt.py | context-protocol prompt |
| print_project_map | src/context_protocol/project_map.py | context-protocol map |

---

## DATA FLOW

### Init Flow

```
┌─────────────────┐
│   User runs     │
│   init command  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ get_templates_  │ ← Find template directory
│ path()          │   (package or repo root)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ shutil.copytree │ ← Copy protocol files to
│ (.context-...)  │   .context-protocol/
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Update/create   │ ← Add @includes to CLAUDE.md
│ CLAUDE.md       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Success msg   │
└─────────────────┘
```

### Doctor Flow

```
┌─────────────────┐
│   User runs     │
│  doctor command │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ load_doctor_    │ ← Load config from .gitignore
│ config()        │   and config.yaml
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ run_doctor()    │ ← Execute 12 health checks
│ - 12 checks     │   Each returns List[DoctorIssue]
└────────┬────────┘
         │ List[DoctorIssue]
         ▼
┌─────────────────┐
│ calculate_      │ ← Compute 0-100 score
│ health_score()  │   based on issue counts
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ generate_health │ ← Create markdown report
│ _markdown()     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Write to SYNC_  │
│ Project_Health  │
└─────────────────┘
```

### Repair Flow

```
┌─────────────────┐
│   User runs     │
│  repair command │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ run_doctor()    │ ← Get current issues
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Filter by depth │ ← links/docs/full
│ and type        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ ThreadPoolExec  │ ← Spawn N parallel agents
│ (parallel)      │
└────────┬────────┘
         │ for each issue
         ▼
┌─────────────────┐
│ spawn_repair_   │ ← Build prompt, run claude
│ agent()         │   subprocess, stream output
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ run_doctor()    │ ← Re-check after repairs
│ (again)         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ generate_final_ │ ← Before/after comparison
│ report()        │
└─────────────────┘
```

---

## LOGIC CHAINS

### LC1: Validation Check Chain

**Purpose:** Run all validation checks and produce results

```
target_dir
  → check_protocol_installed()      # V6
    → check_views_exist()           # V7
      → check_project_sync_exists() # V6
        → check_module_docs_minimum()  # V2
          → check_full_chain()      # FC
            → check_naming_conventions()  # NC
              → check_chain_links() # V3
                → check_module_manifest()  # MM
                  → List[ValidationResult]
```

### LC2: Issue Discovery Chain

**Purpose:** Find all health issues in a project

```
target_dir + config
  → find_source_files()             # Get all code files
    → find_code_directories()       # Find dirs with code
      → doctor_check_monolith()     # Check each file
      → doctor_check_undocumented() # Check module mapping
      → ...12 total checks...
        → List[DoctorIssue]
```

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
    └── imports → doctor_checks.py (all doctor_check_*() functions)
    └── imports → doctor_types.py (DoctorIssue, DoctorConfig)
    └── imports → doctor_report.py (generate_health_markdown, print_doctor_report)
    └── imports → doctor_files.py (load_doctor_config, load_doctor_ignore)
    └── imports → sync.py

doctor_checks.py
    └── imports → doctor_types.py (DoctorIssue, DoctorConfig)
    └── imports → doctor_files.py (should_ignore_path, find_source_files, etc.)
    └── imports → utils.py

repair.py
    └── imports → doctor.py (run_doctor, DoctorIssue)
    └── imports → repair_instructions.py (get_issue_instructions)

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
| Trace logs | `.context-protocol/traces/` | Persistent | Daily files |
| Health report | .context-protocol/state/SYNC_Project_Health.md | Persistent | Overwritten each run |

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
| monolith_lines | .context-protocol/config.yaml (optional) | 500 | Lines threshold for monolith detection |
| stale_sync_days | .context-protocol/config.yaml (optional) | 14 | Days before SYNC is stale |
| ignore | .context-protocol/config.yaml + .gitignore | common patterns | Paths to ignore |
| disabled_checks | .context-protocol/config.yaml (optional) | [] | Checks to skip |

---

## BIDIRECTIONAL LINKS

### Code → Docs

Files that reference this documentation:

| File | Line | Reference |
|------|------|-----------|
| src/context_protocol/cli.py | 4 | DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md |

### Docs → Code

| Doc Section | Implemented In |
|-------------|----------------|
| ALGORITHM: Validate | src/context_protocol/validate.py:667 |
| ALGORITHM: Doctor | src/context_protocol/doctor.py:1160 |
| ALGORITHM: Repair | src/context_protocol/repair.py:970 |
| BEHAVIOR B1: Init | src/context_protocol/init_cmd.py:15 |
| VALIDATION V1 | src/context_protocol/validate.py:33 |

---

## GAPS / IDEAS / QUESTIONS

### Extraction Candidates (Remaining)

Files at SPLIT status need continued decomposition:

| Current File | Lines | Target | Proposed New File | What to Move |
|--------------|-------|--------|-------------------|--------------|
| doctor_checks | ~1732L | <400L | Split by category | Group by check type: doc checks, code checks, config checks |
| repair | ~1384L | <400L | repair_agent (planned) | `spawn_repair_agent()`, agent streaming logic |
| repair_instructions | ~1001L | <400L | Split by category | Group prompts: docs, code, tests |
| validate | ~712L | <400L | validate_checks (planned) | Individual validation check functions |

### Completed Extractions

| Date | Source | Target | Lines Moved |
|------|--------|--------|-------------|
| 2025-12-18 | doctor.py (1900L) | doctor_checks.py | 23 check functions, ~1690L |

### Missing Implementation

- [ ] Add type hints throughout codebase
- [ ] Add DOCS: references to all source files

### Ideas (Not Yet Implemented)

- IDEA: Plugin system for custom checks
- IDEA: Agent prompt templates could be externalized to markdown files
- IDEA: Color/formatting utilities extracted to new file (formatting module)
