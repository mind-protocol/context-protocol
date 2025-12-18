# ADD Framework CLI — Algorithm: Command Processing Logic

```
STATUS: STABLE
CREATED: 2025-12-18
VERIFIED: 2025-12-18 against commit 6e0062c
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Why_CLI_Over_Copy.md
BEHAVIORS:       ./BEHAVIORS_CLI_Command_Effects.md
THIS:            ALGORITHM_CLI_Logic.md (you are here)
VALIDATION:      ./VALIDATION_CLI_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_CLI_Code_Architecture.md
TEST:            ./TEST_CLI_Coverage.md
SYNC:            ./SYNC_CLI_State.md
```

---

## OVERVIEW

The CLI processes commands through a simple dispatch pattern: parse arguments, route to command module, execute, return exit code. The complexity lives in individual commands, particularly `doctor` (health analysis) and `repair` (agent orchestration).

---

## DATA STRUCTURES

### ValidationResult

```
ValidationResult:
  check_id: str          # V1, V2, etc.
  name: str              # Human-readable check name
  passed: bool           # Did check pass?
  message: str           # Summary message
  details: List[str]     # Detailed findings
```

### DoctorIssue

```
DoctorIssue:
  issue_type: str        # MONOLITH, UNDOCUMENTED, etc.
  severity: str          # critical, warning, info
  path: str              # Affected file/directory
  message: str           # Human description
  details: Dict          # Issue-specific details
  suggestion: str        # How to fix
```

### RepairResult

```
RepairResult:
  issue_type: str        # What was being fixed
  target_path: str       # What file/dir
  success: bool          # Did agent succeed?
  agent_output: str      # Full agent output
  duration_seconds: float
  error: Optional[str]   # Error if failed
```

---

## ALGORITHM: Validate Command

### Step 1: Run All Checks

```
results = []
for check in [
    check_protocol_installed,
    check_views_exist,
    check_project_sync_exists,
    check_module_docs_minimum,
    check_full_chain,
    check_naming_conventions,
    check_chain_links,
    check_module_manifest,
]:
    results.append(check(target_dir))
```

### Step 2: Display Results

```
for result in results:
    if result.passed:
        print(f"✓ {result.name}")
    else:
        print(f"✗ {result.name}")
        for detail in result.details:
            print(f"  - {detail}")
```

### Step 3: Generate Fix Guidance

```
if any failures:
    for failed in results:
        print context-specific fix instructions
        print relevant VIEW to load
        print templates to use
```

---

## ALGORITHM: Doctor Command

### Step 1: Load Configuration

```
config = load_doctor_config(target_dir)
  - Parse .gitignore patterns
  - Load config.yaml settings if exists
  - Set thresholds (monolith_lines, stale_sync_days)
```

### Step 2: Run Health Checks

```
all_issues = []
for check in [
    doctor_check_monolith,       # Files > 500 lines
    doctor_check_undocumented,   # Code without docs mapping
    doctor_check_stale_sync,     # SYNC older than 14 days
    doctor_check_placeholder,    # Unfilled templates
    doctor_check_no_docs_ref,    # Source without DOCS: comment
    doctor_check_incomplete_chain,
    doctor_check_broken_impl_links,
    doctor_check_stub_impl,
    doctor_check_incomplete_impl,
    doctor_check_undoc_impl,
    doctor_check_large_doc_module,
    doctor_check_yaml_drift,
]:
    all_issues.extend(check(target_dir, config))
```

### Step 3: Calculate Health Score

```
score = 100
score -= len(critical_issues) * 10
score -= len(warning_issues) * 3
score -= len(info_issues) * 1
score = max(0, score)
```

### Step 4: Save Report

```
markdown = generate_health_markdown(results)
write to .add-framework/state/SYNC_Project_Health.md
```

---

## ALGORITHM: Repair Command

### Step 1: Identify Issues

```
results = run_doctor(target_dir, config)
issues = results.critical + results.warning
filter by depth level (links, docs, full)
filter by explicit type if specified
sort by priority (YAML_DRIFT first, NO_DOCS_REF last)
```

### Step 2: Build Agent Prompts

```
for issue in issues:
    instructions = get_issue_instructions(issue)
    prompt = build_agent_prompt(
        issue=issue,
        view=instructions.view,
        docs_to_read=instructions.docs,
        task_description=instructions.prompt,
    )
```

### Step 3: Spawn Agents (Parallel)

```
with ThreadPoolExecutor(max_workers=parallel) as executor:
    futures = {
        executor.submit(spawn_repair_agent, issue): issue
        for issue in issues
    }
    for future in as_completed(futures):
        result = future.result()
        repair_results.append(result)
```

### Step 4: Execute Agent (per issue)

```
cmd = [
    "claude", "-p", prompt,
    "--dangerously-skip-permissions",
    "--append-system-prompt", AGENT_SYSTEM_PROMPT,
    "--verbose",
    "--output-format", "stream-json",
]
process = subprocess.Popen(cmd, stdout=PIPE)
stream output, parse JSON, show progress
check for "REPAIR COMPLETE" or "REPAIR FAILED"
```

### Step 5: Generate Report

```
run doctor again to get after_results
compare before/after scores
list successful and failed repairs
save to .add-framework/state/REPAIR_REPORT.md
```

---

## KEY DECISIONS

### D1: Depth Filtering

```
IF depth == "links":
    allowed = {NO_DOCS_REF, BROKEN_IMPL_LINK, YAML_DRIFT, UNDOC_IMPL}
    # Safe fixes that only touch references
ELIF depth == "docs":
    allowed = links + {UNDOCUMENTED, STALE_SYNC, PLACEHOLDER, INCOMPLETE_CHAIN, LARGE_DOC_MODULE}
    # Also create/update documentation content
ELSE (full):
    allowed = docs + {MONOLITH, STUB_IMPL, INCOMPLETE_IMPL}
    # Also make code changes
```

### D2: Issue Priority

```
priority_order = {
    YAML_DRIFT: 1,        # Fix manifest first
    BROKEN_IMPL_LINK: 2,  # Then broken refs
    UNDOCUMENTED: 3,      # Then add missing docs
    INCOMPLETE_CHAIN: 4,
    PLACEHOLDER: 5,
    ...
    NO_DOCS_REF: 12,      # Minor fixes last
}
```

---

## DATA FLOW

```
User Command
    ↓
argparse (cli.py)
    ↓
Command Router (cli.py:main)
    ↓
Command Module (e.g., doctor.py)
    ↓
Health Checks / Validation
    ↓
Results Processing
    ↓
Output (stdout + files)
```

---

## COMPLEXITY

**Doctor command:**
- Time: O(n * m) where n = files, m = checks
- Space: O(issues) for storing all findings

**Repair command:**
- Time: O(issues * agent_duration) — agents run in parallel up to limit
- Space: O(parallel * output_size)

**Bottlenecks:**
- File system scanning for monolith/undocumented checks
- Agent execution time (10 min timeout each)
- Parallel agent output interleaving

---

## HELPER FUNCTIONS

### `find_module_directories()`

**Purpose:** Find all doc module directories in docs/

**Logic:** Recursively scan docs/, identify directories containing PATTERNS_/BEHAVIORS_/etc files

### `should_ignore_path()`

**Purpose:** Check if path matches ignore patterns

**Logic:** Match against .gitignore patterns and config.yaml ignore list

### `get_issue_instructions()`

**Purpose:** Generate issue-specific repair instructions

**Logic:** Return VIEW to follow, docs to read, task prompt, success criteria

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| utils.py | `get_templates_path()` | Path to templates |
| utils.py | `find_module_directories()` | List of module dirs |
| doctor.py | `run_doctor()` | Health check results |
| repair.py | `spawn_repair_agent()` | RepairResult |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Consider caching doctor results for faster re-runs
- [ ] Repair could track which issues depend on others
- IDEA: Add --watch flag for continuous monitoring
- QUESTION: Should parallel output be buffered per-agent?
