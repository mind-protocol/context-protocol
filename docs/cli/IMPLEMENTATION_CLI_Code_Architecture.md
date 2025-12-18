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
├── __init__.py         # Package init, empty
├── cli.py              # Entry point, argparse routing
├── init_cmd.py         # Init command implementation
├── validate.py         # Validation checks
├── doctor.py           # Health checks
├── repair.py           # Agent orchestration for repairs
├── sync.py             # SYNC file management
├── context.py          # Code-to-docs navigation
├── prompt.py           # Bootstrap prompt generation
├── project_map.py      # Visual project mapping
├── github.py           # GitHub issue integration
└── utils.py            # Shared utilities
```

### File Responsibilities

| File | Purpose | Key Functions/Classes |
|------|---------|----------------------|
| `src/context_protocol/cli.py` | Entry point, argument parsing | `main()` |
| `src/context_protocol/init_cmd.py` | Protocol initialization | `init_protocol()` |
| `src/context_protocol/validate.py` | Protocol invariant checking | `validate_protocol()`, `ValidationResult` |
| `src/context_protocol/doctor.py` | Project health analysis | `doctor_command()`, `DoctorIssue`, `DoctorConfig` |
| `src/context_protocol/repair.py` | Automated issue fixing | `repair_command()`, `RepairResult`, `spawn_repair_agent()` |
| `src/context_protocol/sync.py` | SYNC file status and archiving | `sync_command()`, `archive_all_syncs()` |
| `src/context_protocol/context.py` | Documentation discovery | `print_module_context()`, `get_module_context()` |
| `src/context_protocol/prompt.py` | LLM prompt generation | `print_bootstrap_prompt()` |
| `src/context_protocol/project_map.py` | Visual dependency map | `print_project_map()` |
| `src/context_protocol/github.py` | GitHub API integration | `create_issues_for_findings()` |
| `src/context_protocol/utils.py` | Shared helpers | `get_templates_path()`, `find_module_directories()` |

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
| doctor_command | src/context_protocol/doctor.py:1629 | context-protocol doctor |
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
    └── imports → utils.py
    └── imports → sync.py

repair.py
    └── imports → doctor.py

validate.py
    └── imports → utils.py
```

### External Dependencies

| Package | Used For | Imported By |
|---------|----------|-------------|
| argparse | CLI parsing | cli.py |
| pathlib | File paths | All files |
| subprocess | Agent spawning | repair.py |
| concurrent.futures | Parallel execution | repair.py |
| yaml (optional) | modules.yaml parsing | utils.py, doctor.py |
| json | JSON output, traces | doctor.py, context.py |
| shutil | File copying | init_cmd.py |
| re | Regex patterns | validate.py, doctor.py |

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

- [ ] Add type hints throughout codebase
- [ ] Consider extracting color/formatting to utils
- [ ] Agent prompt templates could be externalized to files
- IDEA: Plugin system for custom checks
- QUESTION: Should repair agents have access to previous repair results?
