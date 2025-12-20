# ngram Framework CLI — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: codex (escalation rename)
STATUS: CANONICAL
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Why_CLI_Over_Copy.md
BEHAVIORS:       ./BEHAVIORS_CLI_Command_Effects.md
ALGORITHM:       ./ALGORITHM_CLI_Logic.md
VALIDATION:      ./VALIDATION_CLI_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_CLI_Code_Architecture.md
HEALTH:          ./HEALTH_CLI_Coverage.md
THIS:            SYNC_CLI_State.md (you are here)
```

---

## CURRENT STATE

The CLI is stable and in active use. Core commands: `init`, `validate`, `doctor`, `repair`, plus supporting `sync/context/prompt/map/agents`.

---

## IN PROGRESS

No active development at this time.

---

## RECENT CHANGES

### 2025-12-19: Implementation of @ngram:proposition and solve-markers

- Added support for `@ngram:proposition` marker to allow agents to submit ideas/improvements.
- Renamed `ngram solve-escalations` to `ngram solve-markers` to support both escalations and propositions.
- Updated `doctor` to detect both `@ngram:escalation` and `@ngram:proposition` markers via `doctor_check_special_markers`.
- Updated `VIEW_Escalation` and `ALGORITHM_CLI_Logic` documentation to include proposition flow.

### 2025-12-19: Log error health check

- Added a doctor check for recent .log files with error lines (last hour), surfaced as LOG_ERROR issues.
- LOG_ERROR scanning now inspects only the last 2000 lines per recent log file.

### 2025-12-19: Solve escalations command

- Added `ngram solve-escalations` to scan for @ngram escalation markers.
- Scan respects gitignore/ngramignore and skips log files.
- Scan ignores `ngram/solve_escalations.py` and `docs/cli/ALGORITHM_CLI_Logic.md` explicitly.

### 2025-12-19: Escalation terminology rename

- Renamed arbitrage terminology to escalation across CLI commands, repair flow, and docs.

### 2025-12-19: Doctor resolved escalation markers

- Doctor now flags `@ngram:solved-escalations` markers as RESOLVE_ESCALATION issues.

### 2025-12-19: Doctor GitHub issues opt-in

- `ngram doctor` no longer creates GitHub issues by default; use `--github` to enable.

### 2025-12-19: Repair prompt docs preflight

- Repair prompts now note missing docs in a dedicated section so agents can resolve paths before edits.

### 2025-12-19: INCOMPLETE_IMPL verification for repair_core helpers

- Re-verified `ngram/repair_core.py` issue lookup helpers during INCOMPLETE_IMPL repair; no code changes needed

### 2025-12-19: Fix CLI module code path drift

- Updated `modules.yaml` CLI `code` pattern to avoid drift on non-existent `ngram.py`

### 2025-12-19: Sync CLI implementation doc with code structure

- Added newly split doctor checks, repair helpers, and repo overview files
- Updated module dependencies and file responsibilities to match current layout

### 2025-12-19: Fixed broken implementation doc references

- Removed inline backtick references that were misclassified as files
- Updated SVG namespace note to reference `ngram/project_map_html.py`
- Normalized config file paths and key notation in the CLI implementation config table

### 2025-12-19: Externalized overview DOCS header scan length

- `repo_overview.py` now reads DOCS header scan length from DoctorConfig instead of a hardcoded value
- `doctor_files.py` loads `doctor.docs_ref_search_chars` from `.ngram/config.yaml` (default 2000)

### 2025-12-19: Externalized SVG namespace config

- `project_map_html.py` now reads SVG namespace from `.ngram/config.yaml` (`project_map_html.svg_namespace`) with `NGRAM_SVG_NAMESPACE` override
- Added default SVG namespace to `.ngram/config.yaml` for development
- Documented config/env var options in CLI implementation config table

### 2025-12-20: Multi-agent provider support

- `repair` accepts `--agents {claude,codex,gemini}` and `init` mirrors `.ngram/CLAUDE.md` into root `AGENTS.md`

### 2025-12-20: Repair completion uses git commits

- Repair success now keys off git HEAD changes instead of "REPAIR COMPLETE" output markers.
- Agents are instructed not to claim completion without a commit.
- Agent system prompt now requests commit messages with a type prefix and issue reference.
- Repair prompts infer the issue reference from the last 5 commits when not explicitly provided.

### 2025-12-20: Doctor exits cleanly on findings

- `ngram doctor` returns exit code 0 when issues are found

### 2025-12-19: Documentation size reduction

- Reduced `docs/cli` module size by simplifying verbose sections

### 2025-12-19: INCOMPLETE_IMPL false positive review

- Confirmed `get_issue_symbol` and `get_issue_action_parts` already implement lookups
- Re-verified during INCOMPLETE_IMPL repair task; no code changes required

---

## KNOWN ISSUES

- Parallel agent output can intermix during `repair --parallel` (low severity)

---

## CONFLICTS

### DECISION: modules.yaml mapping mismatch
- Conflict: SYNC claims module mapping exists, but `modules.yaml` is template-only.
- Resolution: Keep this documented here; defer mapping to a dedicated task.
- Reasoning: Out of scope for CLI behavior changes.
- Updated: `docs/cli/SYNC_CLI_State.md`

---

## HANDOFF

- Agents: use `VIEW_Extend_Add_Features_To_Existing.md` (new commands) or `VIEW_Debug_Investigate_And_Fix_Issues.md` (bug fixes); no pending work.
- Human: CLI is stable and documented; no input needed.

---

## Agent Observations

### Remarks
- Confirmed INCOMPLETE_IMPL finding was a false positive due to short helper bodies.
- Re-verified `ngram/repair_core.py` issue lookup helpers; implementations already complete.
- SVG namespace now configurable via `NGRAM_SVG_NAMESPACE` for project map HTML output.
- Overview DOCS header scan length now configurable via `doctor.docs_ref_search_chars` in `.ngram/config.yaml`.
- Implementation doc now avoids false broken-link hits from config key notation.
- Added `.ngram/config.yaml` entry for `project_map_html.svg_namespace` with env var override.
- Repair prompts now surface missing docs so agents can resolve paths before edits.
- Doctor now flags recent .log error lines as LOG_ERROR issues.
- Doctor now defaults to no GitHub issue creation unless `--github` is provided.

### Suggestions
- [ ] Reconcile `modules.yaml` with CLI module docs to remove mapping drift.

### Propositions
- No new propositions from this repair.

---

## ARCHIVE

Older content archived to: `SYNC_CLI_State_archive_2025-12.md`
